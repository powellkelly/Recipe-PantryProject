class Pantry:
    
    def __init__(self):
        #Initialize an empty pantry
        self.items = {}
    
    def add_item(self, name, quantity):
        #Adds new items to the pantry + quantity
        name = name.lower()
        
        #Check to see if it already exits
        if name in self.items:
            self.items[name] += quantity
        else:
            self.items[name] = quantity
            
    def update_item(self, name, quantity):
        name = name.lower()
        
        #Remove the item if the quantity is zero
        if quantity == 0:
            self.items.pop(name,None)
        #Otherwise adjust it to the nenw quantity
        else:
            self.items[name] = quantity
            
    def remove_item(self, name, quantity = None):
        name = name.lower()
        
        #If it is not in the pantry ignore
        if name not in self.items:
            return
        
        if quantity is None:
            self.items.pop(name)
        #Subtract the specified quantity
        else:
            self.items[name] -= quantity
            
            #If the quantity becomes zero remove it
            if self.items[name] <= 0:
                self.items.pop(name)
        
    def ingredients_check(self, requirements):
    # Check if the pantry has enough of each required ingredient
    # Returns False immediately if any ingredient is missing or insufficient
    # Returns True if all ingredients meet the required quantity
        for item, required_qty in requirements.items():
            available_qty = self.items.get(item.lower(), 0)
            if available_qty < required_qty:
                return False
            
        return True