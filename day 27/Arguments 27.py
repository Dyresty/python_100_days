#*args is used to pass a variable number of arguments to a function.
#can use * and anm name. like *nums or *vals
def add(*args):

    print(args[1])

    sum = 0
    for n in args:
        sum += n
    return sum

print(add(3, 4, 5, 6, 7, 8, 9))


# **kwargs allows you to pass keyworded variable-length arguments to a function.