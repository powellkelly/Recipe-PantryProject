class Recipe:
    #Initialize a new recipe
    def __init__(self, name, ingredients, instructions, prep_time,calories,
                 vegetarian=False, dairy_free=False, gluten_free=False):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.prep_time = prep_time
        self.calories = calories
        self.vegetarian = vegetarian
        self.dairy_free = dairy_free
        self.gluten_free = gluten_free


recipe_list = [
    Recipe(
        "Simple Pancakes",
        {"flour": 2, "milk": 1, "eggs": 2},
        "Mix all ingredients together. Cook on a pan until golden brown.",
        prep_time=15,
        calories = 350,
        vegetarian=True,
        dairy_free=False,
        gluten_free=False
    ),
    Recipe(
        "Scrambled Eggs",
        {"eggs": 3, "milk": 0.25},
        "Whisk eggs and milk. Cook in a pan while stirring.",
        prep_time=10,
        calories = 350,
        vegetarian=True,
        dairy_free=False,
        gluten_free=True
    ),
    Recipe(
        "Rice Bowl",
        {"rice": 1, "eggs": 1},
        "Cook rice and top with cooked egg.",
        prep_time=20,
        calories = 270,
        vegetarian=True,
        dairy_free=True,
        gluten_free=True
    )
]