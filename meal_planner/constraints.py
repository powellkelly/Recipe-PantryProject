class Constraints:
    def __init__(self):
        #Hard Constraints
        self.vegetarian = False
        self.dairy_free = False
        self.gluten_free = False
        self.max_prep_time = None
        
        #Soft Constraints
        self.activity_level = "moderate"
        self.variety_preference = "medium"
        self.preferred_prep_time = None
        self.target_calories = None
        
        #User profile
        self.sex = None
        self.age = None
        self.weigh_kg = None
        self.height_cm = None
        
    def set_preferences(self):
        print("\n===== User Preferences =====")

        self.vegetarian = input("Vegetarian? (yes/no): ").strip().lower() == "yes"
        self.dairy_free = input("Dairy-free? (yes/no): ").strip().lower() == "yes"
        self.gluten_free = input("Gluten-free? (yes/no): ").strip().lower() == "yes"

        max_time = input("Maximum prep time in minutes (or press Enter to skip): ").strip()
        if max_time:
            self.max_prep_time = int(max_time)

        print("\n===== Calorie Calculation =====")
        self.sex = input("Sex (male/female): ").strip().lower()
        self.age = int(input("Age: ").strip())
        self.weight_kg = float(input("Weight in kg: ").strip())
        self.height_cm = float(input("Height in cm: ").strip())

        print("Activity level options: sedentary, light, moderate, very, extra, athlete")
        activity = input("Activity level: ").strip().lower()
        if activity in ["sedentary", "light", "moderate", "very", "extra", "athlete"]:
            self.activity_level = activity

        self.target_calories = self.calculate_target_calories()

        if self.target_calories is not None:
            print(f"Estimated daily calories: {self.target_calories:.2f}")

        variety = input("Variety preference (low/medium/high): ").strip().lower()
        if variety in ["low", "medium", "high"]:
            self.variety_preference = variety

        preferred_time = input("Preferred prep time in minutes (or press Enter to skip): ").strip()
        if preferred_time:
            self.preferred_prep_time = int(preferred_time)
            
    def calculate_bmr(self):
        if None in [self.sex, self.age, self.weight_kg, self.height_cm]:
            return None

        if self.sex == "male":
            return 66.5 + (13.75 * self.weight_kg) + (5.003 * self.height_cm) - (6.75 * self.age)

        elif self.sex == "female":
            return 655.1 + (9.563 * self.weight_kg) + (1.850 * self.height_cm) - (4.676 * self.age)

        return None

    def calculate_target_calories(self):
        bmr = self.calculate_bmr()

        if bmr is None:
            return None

        activity_factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "very": 1.725,
            "extra": 1.9,
            "athlete": 2.3
        }

        factor = activity_factors.get(self.activity_level, 1.55)
        return bmr * factor
    
    def matches_hard_constraints(self, recipe):
        if self.vegetarian and not recipe.vegetarian:
            return False

        if self.dairy_free and not recipe.dairy_free:
            return False

        if self.gluten_free and not recipe.gluten_free:
            return False

        if self.max_prep_time is not None and recipe.prep_time > self.max_prep_time:
            return False

        return True
        
    def score_recipe(self, recipe):
        score = 0

        if self.preferred_prep_time is not None:
            difference = abs(recipe.prep_time - self.preferred_prep_time)

            if difference <= 5:
                score += 5
            elif difference <= 10:
                score += 3
            else:
                score += 1

        if self.target_calories is not None:
            target_meal_calories = self.target_calories / 3
            calorie_diff = abs(recipe.calories - target_meal_calories)

            if calorie_diff <= 50:
                score += 5
            elif calorie_diff <= 100:
                score += 3
            else:
                score += 1

        return score