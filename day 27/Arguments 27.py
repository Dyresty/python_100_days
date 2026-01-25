#*args is used to pass a variable number of arguments to a function.
#can use * and anm name. like *nums or *vals
# args returns a tuple
def add(*args):

    print(args[1])

    sum = 0
    for n in args:
        sum += n
    return sum

print(add(3, 4, 5, 6, 7, 8, 9))


# **kwargs allows you to pass keyworded variable-length arguments to a function.
# kwargs returns a dictionary
def calculate(n, **kwargs):
    print(kwargs)
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)

calculate(2, add=3, multiply=5)


# Using **kwargs in a class
class Car:
    def __init__(self, **kw):
        self.make = kw.get("make")
        self.model = kw.get("model")
        self.year = kw.get("year")
        self.color = kw.get("color")

my_car = Car(make="Nissan", model="GT-R", year=2020, color="White")
print(my_car.model)


# Combining *args and **kwargs
def all_aboard(a, *args, **kw): 
    print(a, args, kw)

all_aboard(4, 7, 3, 0, x=10, y=64)