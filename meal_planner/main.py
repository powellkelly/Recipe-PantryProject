# Import the Pantry class,
# recipe object, and constraints class
import json
import os
from pantry import Pantry
from recipes import recipe_list
from constraints import Constraints

PANTRY_FILE = "pantries.json"

def load_all_pantries():
    if os.path.exists(PANTRY_FILE):
        with open(PANTRY_FILE, "r") as file:
            return json.load(file)
    return {}

def save_all_pantries(all_pantries):
    with open(PANTRY_FILE, "w") as file:
        json.dump(all_pantries, file, indent=4)

def load_pantry_by_name(name, constraints):
    all_pantries = load_all_pantries()
    pantry = Pantry()

    if name in all_pantries:
        data = all_pantries[name]

        pantry.items = data.get("items", {})

        prefs = data.get("preferences", {})
        constraints.vegetarian = prefs.get("vegetarian", False)
        constraints.dairy_free = prefs.get("dairy_free", False)
        constraints.gluten_free = prefs.get("gluten_free", False)
        constraints.max_prep_time = prefs.get("max_prep_time", None)
        constraints.preferred_prep_time = prefs.get("preferred_prep_time", None)
        constraints.target_calories = prefs.get("target_calories", None)

    return pantry

def save_pantry_by_name(name, pantry, constraints):
    all_pantries = load_all_pantries()

    all_pantries[name] = {
        "items": pantry.items,
        "preferences": {
            "vegetarian": constraints.vegetarian,
            "dairy_free": constraints.dairy_free,
            "gluten_free": constraints.gluten_free,
            "max_prep_time": constraints.max_prep_time,
            "preferred_prep_time": constraints.preferred_prep_time,
            "target_calories": getattr(constraints, "target_calories", None)
        }
    }

    save_all_pantries(all_pantries)

# Allows user to enter items into their pantry
def enter_pantry_items(pantry):
    print("\n===== Pantry Entry =====\n")

    # Guidelines for how to enter quantities
    print("Measurement Guidelines:")
    print("- Liquids (milk, oil, etc.) -> enter quantity in cups")
    print("- Whole items (eggs, apples, etc.) -> enter as a count (just the number)")
    print("- Dry ingredients (flour, sugar, rice, etc.) -> enter quantity in cups\n")

    # Asks user to enter ingredient name & quantity
    while True:
        name = input("Ingredient name: ").strip()

        # Break if user enters done
        if name.lower() == "done":
            break

        try:
            quantity = float(input("Quantity: ").strip())
            # Add item to pantry
            pantry.add_item(name, quantity)
        except ValueError:
            print("Please enter a valid number for quantity.\n")

# Show current contents of pantry if any
def display_pantry(pantry):
    print("\n===== Current Pantry =====")

    if not pantry.items:
        print("Pantry is empty")
    else:
        # Sort items alphabetically for readability
        for item, quantity in sorted(pantry.items.items()):
            # Show whole numbers without .0
            if quantity == int(quantity):
                quantity = int(quantity)

            # Show units for clarity
            if item in ["milk", "oil"]:
                print(f"{item}: {quantity} cups")
            elif item in ["eggs"]:
                print(f"{item}: {quantity} count")
            else:
                print(f"{item}: {quantity} cups")

def main():
    print("1. Start a new pantry")
    print("2. Load an existing pantry")

    choice = input("Choose an option (1 or 2): ").strip()
    pantry_name = input("Enter pantry name: ").strip()

    constraints = Constraints()

    if choice == "2":
        all_pantries = load_all_pantries()
        if pantry_name in all_pantries:
            pantry = load_pantry_by_name(pantry_name, constraints)
            print(f"\nLoaded pantry: {pantry_name}")
        else:
            print("\nPantry not found. Creating a new pantry instead.")
            pantry = Pantry()
    else:
        pantry = Pantry()
        print(f"\nCreated new pantry: {pantry_name}")

    # Ask for preferences only if not already saved
    if constraints.target_calories is None:
        constraints.set_preferences()
    else:
        print("\nLoaded saved preferences.")

    # User enters pantry items
    enter_pantry_items(pantry)

    # Save pantry + preferences
    save_pantry_by_name(pantry_name, pantry, constraints)

    # Show pantry
    display_pantry(pantry)

    # Store recipes and their scores
    ranked_recipes = []

    for recipe in recipe_list:
        has_ingredients = pantry.ingredients_check(recipe.ingredients)
        fits_constraints = constraints.matches_hard_constraints(recipe)

        if has_ingredients and fits_constraints:
            score = constraints.score_recipe(recipe)
            ranked_recipes.append((recipe, score))

    if not ranked_recipes:
        print("\n*** No recipes match your pantry and/or constraints ***")
        return

    ranked_recipes.sort(key=lambda x: x[1], reverse=True)

    print("\n===== Recommended Recipes =====")
    for i, (recipe, score) in enumerate(ranked_recipes, start=1):
        print(f"{i}. {recipe.name} ({recipe.prep_time} min, {recipe.calories} cal, score: {score})")
        print(f"   Instructions: {recipe.instructions}")

    answer = input("\nWould you like to make one of these recipes? (yes/no): ").strip().lower()

    if answer == "yes":
        try:
            choice = int(input("Enter the recipe number: ").strip())

            if 1 <= choice <= len(ranked_recipes):
                chosen_recipe = ranked_recipes[choice - 1][0]

                for item, quantity in chosen_recipe.ingredients.items():
                    pantry.remove_item(item, quantity)

                # Save updated pantry to file
                save_pantry_by_name(pantry_name, pantry, constraints)

                print(f"\n*** You made {chosen_recipe.name}! Pantry has been updated. ***")
                display_pantry(pantry)
            else:
                print("\nInvalid recipe number")

        except ValueError:
            print("\nPlease enter a valid number")

if __name__ == "__main__":
    main()