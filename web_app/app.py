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
    return render_template('index.html')


@app.route('/goals', methods=['GET', 'POST'])  # Accept both GET and POST methods
def goals():
  if request.method == 'POST':
      session['time'] = request.form.get('time')
      session['budget'] = request.form.get('budget')
      session['people'] = int(request.form.get('people'))
      servingsPerDay = int(request.form.get('servingsPerDay'))
      session['maxServings'] = 7 * session.get('people') * servingsPerDay
      session['zipCode'] = request.form.get('zipCode')

      return redirect(url_for('menu'))

  return render_template('goals.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    
  time = session.get('time')
  budget = float(session.get('budget'))
  maxServings = int(session.get('maxServings'))
  people = int(session.get('people'))
  servingsPerPerson = int(maxServings / people)
  meals = Meal.query.order_by(Meal.unit_price).all()
  total_servings = request.form.get('totalServings')
  time_used = request.form.get('timeUsed')
  money_spent = request.form.get('moneySpent')
  
  if time_used is not None and money_spent is not None:
    session['timeUsed'] = int(time_used)
    session['moneySpent'] = float(money_spent)
  else:
    session['timeUsed'] = 0
    session['moneySpent'] = 0

    
  
  selected_ids = []


  if request.method == 'POST':
      selected_ids = request.form.getlist('selected_meals')
      
      if (int(total_servings) >= servingsPerPerson):
        meal_quantities = {}

        for id in selected_ids:
          servings = request.form.get('servings' + id)
          meal_quantities[id] = int(servings)
          # servings is returning None on broccoli quich
        session['meal_quantities'] = meal_quantities
        return redirect(url_for('plan'))
      else:
        return render_template('menu.html', time=time, budget=budget, maxServings=maxServings,
                                 meals=meals, people=people, servingsPerPerson=servingsPerPerson, selected_ids=selected_ids,
                                 error_message=f"You still need {servingsPerPerson - int(total_servings)} servings! Select meals again and increase servings.")

  return render_template('menu.html', time=time, budget=budget, maxServings=maxServings, meals=meals,
                         people=people, servingsPerPerson=servingsPerPerson, selected_ids=selected_ids,
                         error_message="")

  
  
  
  
  
  
@app.route('/plan', methods=['GET', 'POST'])
def plan():
  meal_quantities = session.get('meal_quantities')
  selected_meals = Meal.query.filter(Meal.id.in_(meal_quantities.keys())).all()
  timeUsed = int(session.get('timeUsed'))
  moneySpent = int(session.get('moneySpent'))
  budget=float(session.get('budget'))
  time=int(session.get('time'))
  money_result = int(budget - moneySpent)
  time_result = int(time - timeUsed)
  units_not_used = ["cups", "cup", "tsp", "tbsp"]
  #meal_quant = {'id'=}
  
  shopping_list ={}
  
  for meal_id, servingsPerPerson in meal_quantities.items():
      meal = Meal.query.get(meal_id)

      ingredients = dict(json.loads(meal.ingredients))

      for ingredient, ingredient_values in ingredients.items():
        if ingredient not in shopping_list:
          if ingredient_values["unit"] in units_not_used:
            shopping_list[ingredient] = {"unit": "", "quantity" : ""}
          else: 
            shopping_list[ingredient] = {"unit": ingredient_values["unit"], "quantity" : float(ingredient_values["quantity"])/meal.servings*servingsPerPerson*session.get('people')}
        else:
          if ingredient_values["quantity"] != "" and shopping_list[ingredient]["quantity"] != "":
            shopping_list[ingredient]["quantity"] += float(ingredient_values["quantity"])/meal.servings*servingsPerPerson*session.get('people')
  for item in shopping_list.keys():
    if(shopping_list[item]["quantity"] != ""):
      
      shopping_list[item]["fraction"] = Fraction(round(shopping_list[item]["quantity"]*2)/2).limit_denominator()
  
  return render_template('plan.html', selected_meals=selected_meals, shopping_list=shopping_list, money_result=money_result , time_result=time_result, moneySpent=moneySpent, timeUsed=timeUsed, money_over = -money_result, time_over = -time_result)



if __name__ == "__main__":
  app.run(debug=True)
