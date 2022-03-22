import Sdecorators


@Sdecorators.JsonSaveReturn("./test.json", "decorator_result")
@Sdecorators.Repeater(3)
@Sdecorators.IgnoreException()
@Sdecorators.RunTimeMonitor()
@Sdecorators.InvokeCount()
@Sdecorators.ShowFunctionDetail()
@Sdecorators.DecorateTheReturn(str)
@Sdecorators.DecorateTheParameters(int)
@Sdecorators.JsonReadData("./data.json", "first_number")
def decorator_test(a, b):
    print('starting')

    return a * b


@Sdecorators.Repeater(1, 6, 2)
@Sdecorators.JsonSaveReturn()
def repeat(name):
    print("repeat !!")
    return f"{name} repeat !!"


@Sdecorators.JsonSaveReturn("./test.json")
@Sdecorators.JsonReadData("./data.json", "second_number", 1,lambda x : x > 100)
@Sdecorators.JsonReadData("./data.json", "first_number", 0)
def a(b, c):
    return b * c


print(a("a", 120))
# print(repeat("uu"))
print(decorator_test(5,3))
