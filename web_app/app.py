from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv
import os
from fractions import Fraction

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/meals.db'
db = SQLAlchemy(app)

class Meal(db.Model):
  """
  Create a model for the database with necessary field information
  """
  __tablename__ = 'meals'

  id = db.Column(db.Integer, primary_key=True)  # Primary key
  name = db.Column(db.String, nullable=False)  # Meal name
  servings = db.Column(db.Integer)  # Number of servings
  unit_price = db.Column(db.Float)  # Price per unit
  prep = db.Column(db.Integer)  # Preparation time
  ingredients = db.Column(db.Text)  # Ingredients list
  url = db.Column(db.String)  # URL for the meal

@app.route('/')
def home():
  """
  Home page for the website
  """
  return render_template('index.html')


@app.route('/goals', methods=['GET', 'POST'])
def goals():
  """
  Page for the user to set their budget goals for the week's meals
  """
  if request.method == 'POST':
    # Retrieve the information and store it in the session
    session['time'] = request.form.get('time')
    session['budget'] = request.form.get('budget')
    session['people'] = int(request.form.get('people'))
    servings_per_day = int(request.form.get('servingsPerDay'))
    session['max_servings'] = 7 * session.get('people') * servings_per_day # Total number of servings for a week given number of daily servings and quantity of people
    session['zip_code'] = request.form.get('zipCode') # For future use with API integration
    
    # Move to menu selection page
    return redirect(url_for('menu'))

  return render_template('goals.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
  """
  Menu page where the user selects meals based on their goals made previously
  """
  # Retrieve information from session for logic
  time = session.get('time')
  budget = float(session.get('budget'))
  max_servings = int(session.get('max_servings'))
  people = int(session.get('people'))
  
  servings_per_person = int(max_servings / people)
  
  # Get all meals ordered by price from the database
  meals = Meal.query.order_by(Meal.unit_price).all()
  
  # Grab the current numbers from the user
  total_servings = request.form.get('totalServings')
  time_used = request.form.get('timeUsed')
  money_spent = request.form.get('moneySpent')
  
  # Check how much time and money is used, if none, set to zero
  if time_used is not None and money_spent is not None:
    session['timeUsed'] = int(time_used)
    session['moneySpent'] = float(money_spent)
  else:
    session['timeUsed'] = 0
    session['moneySpent'] = 0

  # List for the IDs of meals selected
  selected_ids = []

  if request.method == 'POST':
      
      # Add to the list all meals that have been selected
      selected_ids = request.form.getlist('selected_meals')
      
      # If the user has selected enough meals and servings with the week proceed
      # Otherwise, return an message asking to start over and select more
      if (int(total_servings) >= servings_per_person):
        
        # Dictionary to store the quantity of each meal
        meal_quantities = {}
        
        for id in selected_ids:
          servings = request.form.get('servings' + id)
          meal_quantities[id] = int(servings)
          
        session['meal_quantities'] = meal_quantities
        
        return redirect(url_for('plan'))
      else:
        return render_template('menu.html', time=time, budget=budget,
                                 meals=meals, people=people, servingsPerPerson=servings_per_person, selected_ids=selected_ids,
                                 error_message=f"You still need {servings_per_person - int(total_servings)} servings! Start over and select meals again and increase servings.")

  return render_template('menu.html', time=time, budget=budget, meals=meals,
                         people=people, servingsPerPerson=servings_per_person, selected_ids=selected_ids,
                         error_message="")


@app.route('/plan', methods=['GET', 'POST'])
def plan():
  """
  Plan page where the user recieves the final total and their shopping list as well as links to recipes
  """
  
  
  def rounded_mixed_number(num):
    """
    Function to round a fraction to a reasonable mixed number for cooking
    """
    rounded_num = int(num)
    fraction = num-rounded_num
    rounded_fraction = round(fraction*2)/2
    if rounded_fraction == 1:
      return str(rounded_num +1)
    elif rounded_fraction == 0:
      return str(rounded_num)
    else:
      if rounded_num == 0:
        return str(Fraction(rounded_fraction).limit_denominator())
      else:
        return str(rounded_num)+ " " + str(Fraction(rounded_fraction).limit_denominator())
  
  meal_quantities = session.get('meal_quantities')
  selected_meals = Meal.query.filter(Meal.id.in_(meal_quantities.keys())).all()
  timeUsed = int(session.get('timeUsed'))
  moneySpent = int(session.get('moneySpent'))
  budget=float(session.get('budget'))
  time=int(session.get('time'))
  money_result = int(budget - moneySpent)
  time_result = int(time - timeUsed)
  units_not_used = ["cups", "cup", "tsp", "tbsp"]
  quantity_list = [session.get('people')*quantity for quantity in meal_quantities.values()]
  selected_count = len(selected_meals)
  
  shopping_list ={}
  
  for meal_id, servings_per_person in meal_quantities.items():
      meal = Meal.query.get(meal_id)
      ingredients = dict(json.loads(meal.ingredients))

      for ingredient, ingredient_values in ingredients.items():
        if ingredient not in shopping_list:
          if ingredient_values["unit"] in units_not_used:
            shopping_list[ingredient] = {"unit": "", "quantity" : ""}
          else: 
            shopping_list[ingredient] = {"unit": ingredient_values["unit"], "quantity" : float(ingredient_values["quantity"])/meal.servings*servings_per_person*session.get('people')}
        else:
          if ingredient_values["quantity"] != "" and shopping_list[ingredient]["quantity"] != "":
            shopping_list[ingredient]["quantity"] += float(ingredient_values["quantity"])/meal.servings*servings_per_person*session.get('people')
  
  for item in shopping_list.keys():
    if(shopping_list[item]["quantity"] != ""):
      if (shopping_list[item]["unit"] == "lb."):
        shopping_list[item]["fraction"] = round(shopping_list[item]["quantity"], 2)
      else:
        shopping_list[item]["fraction"] =  rounded_mixed_number(shopping_list[item]["quantity"])
  
  return render_template('plan.html', selected_meals=selected_meals,  shopping_list=shopping_list, money_result=money_result , time_result=time_result, moneySpent=moneySpent, timeUsed=timeUsed, money_over = -money_result, time_over = -time_result, selected_count=selected_count, quantity_list=quantity_list)


if __name__ == "__main__":
  app.run(debug=True)
