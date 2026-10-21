# this is my introduction class object in python
class Pizza:
    # define the function for the class
    def __init__(self, crust, toppings):
        # self is the variable define for this class
        # __init__ initialize the input argument
        self.crust = crust
        self.toppings = toppings

    def order(self):
        return f'Your {self.crust} {self.toppings} pizza is ready'

pizza = Pizza('thin', 'Hawaiian')
print(pizza.order())