from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


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
      time = request.form.get('time')
      budget = request.form.get('budget')
      people = int(request.form.get('people'))
      servingsPerDay = int(request.form.get('servingsPerDay'))
      maxServings = 7 * people * servingsPerDay
      zipCode = request.form.get('zipCode')

      return redirect(url_for('menu', time=time, budget=budget, maxServings=maxServings, zipCode=zipCode, people=people))

  return render_template('goals.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':

        selected_ids = request.form.getlist('selected_meals') 
        zipCode = request.args.get('zipCode')
        # return render_template('test.html', value=selected_meals)
        return redirect(url_for('plan', selected_ids=','.join(selected_ids),zipCode=zipCode))
    meals = Meal.query.all()
    time = request.args.get('time')
    budget = float(request.args.get('budget'))
    maxServings = int(request.args.get('maxServings'))
    people = int(request.args.get('people'))
    zipCode = request.args.get('zipCode')
    servingsPerPerson = int(maxServings/people)
    return render_template('menu.html', time=time, budget=budget, maxServings=maxServings, meals=meals, people=people, servingsPerPerson=servingsPerPerson)


@app.route('/plan', methods=['GET', 'POST'])
def plan():
  selected_ids = request.args.get('selected_ids').split(',')
  selected_meals = Meal.query.filter(Meal.id.in_(selected_ids)).all()
  shopping_list ={}
  # for each meal
  #  look at ingrdients and quantities
  #    if ingredient not in shopping list add it
  #      if unit is not tsp, tbsp, cup add quantity with unit
  #    else if has quanitiy, quanitiy += ingredient quanitity
  
  # pass in shopping list
  
  for meal in selected_meals:
    for ingredient in meal.ingredients:
      if ingredient not in shopping_list:
        if ingredient.unit != "cup" or ingredient.unit != "tsp" or ingredient.unit != "tbps":
          shopping_list[ingredient] = {ingredient.}
  
  
  
  return render_template('plan.html', selected_meals=selected_meals, shopping_list=shopping_list)



if __name__ == "__main__":
  app.run(debug=True)
