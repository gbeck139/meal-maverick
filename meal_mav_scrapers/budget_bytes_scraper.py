import json
import unicodedata

import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


def parse_quantity(input_string):
    parts = input_string.split("-")[0].split(" ")
    if len(parts) == 1:
        if "/" in parts[0]:
            parts = parts[0].split("/")
            return float(parts[0])/float(parts[1])
        if "." in parts[0]:
            return float(parts[0])
        if len(parts[0]) > 1:
            return float(parts[0])
        return float(unicodedata.numeric(parts[0]))
    elif len(parts) == 2:
        integer_part = float(parts[0])
        fractional_part = parse_quantity(parts[1])
        return integer_part + fractional_part
    else:
        raise ValueError("Input string is not in the correct format.")


# Step 2: Scrape the website
def scrape_website():
    options = Options()
    options.headless = False  # Set to False if you want to see the browser
    driver = webdriver.Chrome(options=options)
    meals = []

    for i in range(1):
        time.sleep(2)
        url = f"https://www.budgetbytes.com/category/extra-bytes/budget-friendly-meal-prep/page/{i}"
        driver.get(url)

        # Get the page source
        page_source = driver.page_source

        # Print the page source (you can also parse it)
        soup = BeautifulSoup(page_source, 'html.parser')
        count = 0
        for meal_info in soup.find_all("article", {"class": "post-summary post-summary--default"}):
            name = meal_info.find("h3", class_="post-summary__title").text.strip()
            unit_price = float(meal_info.find("span", class_="cost-per").text.strip().split('$')[-1].split(" ")[0])
            recipe_url = meal_info.find("a")["href"]
            print_url = recipe_url[:28]+"wprm_print/" + recipe_url[28:]
            time.sleep(2)
            driver.get(recipe_url)
            # driver.get("https://www.budgetbytes.com/turkey-pinwheels/")
            recipe = driver.page_source
            recipe_soup = BeautifulSoup(recipe, 'html.parser')

            header_soup = recipe_soup.find("div", class_="bb-recipe-card__meta")
            prep = int(header_soup.find("span", class_="wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes").text.strip().split(" ")[0])
            servings = int(header_soup.find("input")["value"])

            ingredients = {}
            for ingredient_soup in recipe_soup.find_all("li", class_="wprm-recipe-ingredient"):
                ingredient_name = ingredient_soup.find("span", class_="wprm-recipe-ingredient-name").text.strip().replace("*", "").split(",")[0].split(" (")[0]
                ingredient_quantity = ingredient_soup.find("span", class_="wprm-recipe-ingredient-amount")
                if ingredient_quantity is None:
                    continue
                else:
                    ingredient_quantity = ingredient_quantity.text.strip()
                ingredient_unit = ingredient_soup.find("span", class_="wprm-recipe-ingredient-unit")
                if ingredient_unit is None:
                    ingredient_unit = ""
                else:
                    ingredient_unit = ingredient_unit.text.strip().lower()
                ingredient_estimated_price = ingredient_soup.find("span", class_="wprm-recipe-ingredient-notes wprm-recipe-ingredient-notes-normal")
                if ingredient_estimated_price is None:
                    ingredient_estimated_price = 0
                else:
                    ingredient_estimated_price = ingredient_estimated_price.text.strip()
                    if "$" not in ingredient_estimated_price:
                        continue
                    else:
                        ingredient_estimated_price = ingredient_estimated_price[2:-1]
                ingredients[ingredient_name] = {}
                print(ingredient_name)
                ingredients[ingredient_name]["quantity"] = parse_quantity(ingredient_quantity)
                ingredients[ingredient_name]["price"] = float(ingredient_estimated_price)
                ingredients[ingredient_name]["unit"] = ingredient_unit

            print(f"Name: {name}\nServings: {servings}\nServing price: {unit_price}\nPrep: {prep}\nIngredients: {ingredients}\nURL: {print_url}")
            meal = {"name": name, "servings": servings, "unit_price": unit_price, "prep": prep,
                    "ingredients": ingredients, "url": print_url}
            meals.append(meal)
    driver.quit()
    return meals

# Main execution
if __name__ == "__main__":
    connection = sqlite3.connect('../meals.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            servings INTEGER,
            unit_price Real,
            prep INTEGER,
            ingredients TEXT,
            url TEXT
        )
    ''')
    connection.commit()

    meals = scrape_website()  # Scrape the website for meal data

    for meal in meals:
        cursor.execute('''
            INSERT INTO meals (name, servings, unit_price, prep, ingredients, url) VALUES (?, ?, ?, ?, ?, ?)
        ''', (meal["name"], meal["servings"], meal["unit_price"], meal["prep"], json.dumps(meal["ingredients"]), meal["url"]))
        connection.commit()

    connection.close()