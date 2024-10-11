from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
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

  
  
    if request.method == 'POST':
        selected_ids = request.form.getlist('selected_meals') 
        
        if not selected_ids:
          return render_template('menu.html', time=time, budget=budget, maxServings=maxServings,
                                   meals=meals, people=people, servingsPerPerson=servingsPerPerson,
                                   error_message="Please select at least one meal.")
        else:
          meal_quantities = {}
          
          for id in selected_ids:
            servings = request.form.get('servings' + id)
            meal_quantities[id] = servings
          
          return redirect(url_for('plan', mealQuantities=json.dumps(meal_quantities)))
        
    return render_template('menu.html', time=time, budget=budget, maxServings=maxServings,
                           meals=meals, people=people, servingsPerPerson=servingsPerPerson,
                           error_message="")
    
  
  
  
  
  
  
@app.route('/plan', methods=['GET', 'POST'])
def plan():
  meal_quantities = json.loads(request.args.get('mealQuantities'))
  selected_meals = Meal.query.filter(Meal.id.in_(meal_quantities_ids)).all()
  shopping_list ={}
  # for each meal
  #  look at ingrdients and quantities
  #    if ingredient not in shopping list add it
  #      if unit is not tsp, tbsp, cup add quantity with unit
  #    else if has quanitiy, quanitiy += ingredient quanitity
  
  # pass in shopping list
  
  for meal in selected_meals:
    ingredients = dict(json.loads(meal.ingredients))
    
    for ingredient, values in ingredients.items():
      if ingredient not in shopping_list:
        # if values["unit"] == "cup" or values["unit"] == "tsp" or values["unit"] == "tbsp":
        shopping_list[ingredient] = {"unit": values["unit"], "quantity" : int(values["quantity"])}
      else:
        if values["quantity"] != "":
          shopping_list[ingredient]["quantity"] += int(values["quantity"])
  
  
  return render_template('plan.html', selected_meals=selected_meals, shopping_list=shopping_list)



if __name__ == "__main__":
  app.run(debug=True)
