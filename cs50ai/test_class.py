class MyClass:
    i = 123
    def f (self):
        return 'Hello'

x = MyClass()
print(x.i)

# used init to be able to pass in argument
class MyClass1:

    # toppings = [] # example of a class variable
    
    def __init__(self, number, phrase): # self has to be the first argument
        self.num = number
        self.phrase = phrase

x = MyClass1(645, 'TobyPie') # x is passed into the method as the first agrument
print(f'My number is {x.num} and my phrase is {x.phrase}')

class Pizza:
    def __init__ (self, crust):
        self.crust = crust
        self.toppings = []

    def add_topping (self, toppings):
        self.toppings.append(toppings) # can call variables and data types from other methods

    def assemble(self):
        string = f'Your pizza order is {self.crust} crust with '
        for i in self.toppings:
            string += i
        return string

my_order = Pizza('thin')
my_order.add_topping('pineapple and ham')
print(my_order.assemble())

