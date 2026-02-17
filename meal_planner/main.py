# Import the Pantry class and sample_recipe object
from pantry import Pantry
from recipes import sample_recipe

# Allows user to enter items into their pantry
def enter_pantry_items(pantry):
    print("\n===== Pantry Entry =====\n")
    
    # Guidelines for how to enter quantities
    print("Measurement Guidelines:")
    print("- Liquids (milk, oil, etc.) → enter quantity in cups")
    print("- Whole items (eggs, apples, etc.) → enter as a count (just the number)")
    print("- Dry ingredients (flour, sugar, rice, etc.) → enter quantity in cups\n")

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
            print("Please enter a valid number for quantity. \n")

# Show current contents of pantry if any
def display_pantry(pantry):
    print("\n===== Current Pantry =====")
    
    if not pantry.items:
        print("Pantry is empty")
    else:
        # Sort items alphabetically for readability
        for item, quantity in sorted(pantry.items.items()):
            # Show units for clarity
            if item in ["milk", "oil"]:
                print(f"{item}: {quantity} cups")
            elif item in ["eggs"]:
                print(f"{item}: {quantity} count")
            else:
                print(f"{item}: {quantity} cups")

def main():
    # Create new pantry object
    pantry = Pantry()
    
    # User enters pantry items
    enter_pantry_items(pantry)
    # Show what is currently in the pantry
    display_pantry(pantry)

    # Check if the pantry has enough ingredients for the recipe
    if pantry.ingredients_check(sample_recipe.ingredients):
        # Display recipe with a heading
        print("\n===== Recipe Suggestion =====")
        print(f"You can make: {sample_recipe.name}")
        print("Ingredients needed:")
        for i, (item, quantity) in enumerate(sample_recipe.ingredients.items(), start=1):
            print(f"{i}. {item}: {quantity}")
        print(f"\nInstructions: {sample_recipe.instructions}\n")
    else:
        # Tell user they cannot make this recipe
        print("\n*** You do not have all the ingredients to make this recipe ***\n")
        return  # Exit if recipe cannot be made

    # Ask if user wants to make the recipe
    answer = input("Would you like to make this recipe? (yes/no): ").strip().lower()
    if answer == "yes":
        # Subtract used ingredients from the pantry
        for item, quantity in sample_recipe.ingredients.items():
            pantry.remove_item(item, quantity)
        print(f"\n*** You made {sample_recipe.name}! Pantry has been updated. ***")

    # Show updated pantry
    display_pantry(pantry)
    
if __name__ == "__main__":
    main()
