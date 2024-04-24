def hi(name='123'):
    return "hi"+name
print(hi())
greet=hi
print(greet())
del hi
print(greet())