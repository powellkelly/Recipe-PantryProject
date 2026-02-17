class Recipe:
    #Initialize a new recipe
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        
#Sample test recipe
sample_recipe = Recipe(
    "Simple Pancakes",
    {
        "flour": 2,
        "milk": 1,
        "eggs": 2
    },
    "Mix all ingredients togther. Cook on a pan until golden brown"
)
    
        
