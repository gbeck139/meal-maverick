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

        budget = request.form.get('budget')
        preferences = request.form.get('preferences')
        zip_code = request.form.get('zipCode')

        return redirect(url_for('menu', budget=budget, preferences=preferences, zipCode=zip_code))

    return render_template('goals.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':

        selected_ids = request.form.getlist('selected_meals') 
        selected_meals = Meal.query.filter(Meal.id.in_(selected_ids)).all()
        return redirect(url_for('plan', selected_meals=selected_meals))
    meals = Meal.query.all()
    budget = request.args.get('budget')
    preferences = request.args.get('preferences')
    zip_code = request.args.get('zipCode')
    return render_template('menu.html', budget=budget, preferences=preferences, zip_code=zip_code, meals=meals)


@app.route('/plan')
def plan():
  selected_meals = request.args.get('selected_meals')
  return render_template('plan.html', selected_meals=selected_meals)



if __name__ == "__main__":
  app.run(debug=True)
