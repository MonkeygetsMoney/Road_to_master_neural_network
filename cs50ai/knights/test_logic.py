# testing the the syntax and function from logic module
from cs50ai.knights.logic import *

Aknight = Symbol('A is a knight')
Aknave = Symbol('A is a knave')

statement = And(Aknight, Aknave)
print(statement)