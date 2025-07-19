# Meal Maverick

Meal Maverick is a web application designed to streamline weekly meal planning. It cuts planning time from over 30 minutes to less than 5 by providing users with a curated library of budget-friendly recipes and generating a precise shopping list with a single click. This not only saves time and money but also helps to reduce food waste.

<br>

## Tech Stack

**Backend:** Python, Flask, Flask-SQLAlchemy  
**Database:** SQLite  
**Web Scraping:** Selenium, Beautiful Soup  
**Frontend:** HTML, CSS, JavaScript

<br>

## Key Features

* **Goal Setting:** Users can define their weekly meal prep goals, including budget, available time, and the number of people to feed.
* **Dynamic Meal Selection:** A menu of recipes, populated by a web scraper, is presented to the user, ordered by price. As the user selects meals, the estimated total cost and prep time are updated in real-time with dynamic progress bars.
* **Automated Shopping List:** Once the user finalizes their meal plan, the application generates a consolidated shopping list. It intelligently calculates the precise quantity of each ingredient needed, preventing over-buying and food waste.
* **Recipe Links:** The final plan includes direct links to the original recipes for easy access during cooking.

<br>

## Setup and Installation

To run Meal Maverick locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/gbeck139/meal-maverick.git](https://github.com/gbeck139/meal-maverick.git)
    cd meal-maverick
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    The project uses a `Pipfile` to manage dependencies. Install `pipenv` first if you don't have it:
    ```bash
    pip install pipenv
    pipenv install
    ```
    Alternatively, you can use the `requirements.txt` in the `web_app` directory:
    ```bash
    pip install -r web_app/requirements.txt
    ```

4.  **Populate the database:**
    Run the web scraper to populate the SQLite database with recipes.
    ```bash
    cd meal_mav_scrapers
    python budget_bytes_scraper.py
    ```

5.  **Run the Flask application:**
    ```bash
    cd ../web_app
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

<br>

## Technical Highlights

* **Web Scraper:** The project utilizes a Selenium scraper to navigate paginated content on *budgetbytes.com*. It extracts recipe details, including name, prep time, servings, and a detailed ingredient list, and then populates the `meals.db` SQLite database.
* **Ingredient Calculation Logic:** A key feature of the application is its ability to calculate the exact amount of each ingredient for the shopping list. The Flask backend processes the user's selected meals and servings, aggregates the required ingredients, and even converts quantities into user-friendly fractions for easier use in the kitchen.
* **Dynamic Frontend:** The menu page provides real-time feedback to the user. As meals are selected, JavaScript updates progress bars for the budget and prep time, giving instant insight into how their choices align with their goals.

<br>

## Future Development

* **Store API Integration:** The application includes a placeholder for ZIP code input, with plans to integrate with a store API for localized pricing and online shopping cart functionality.
