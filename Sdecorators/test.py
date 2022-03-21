import Sdecorators


@Sdecorators.JsonSaveReturn("./test.json", "decorator_result")
@Sdecorators.Repeater(3)
@Sdecorators.IgnoreException()
@Sdecorators.RunTimeMonitor()
@Sdecorators.InvokeCount()
@Sdecorators.ShowFunctionDetail()
@Sdecorators.DecorateTheReturn(str)
@Sdecorators.DecorateTheParameters(int)
def decorator_test(a, b):
    print('starting')

    return a * b


@Sdecorators.Repeater(1, 6, 2)
@Sdecorators.JsonSaveReturn()
def repeat(name):
    print("repeat !!")
    return f"{name} repeat !!"


@Sdecorators.JsonSaveReturn("./test.json", "test_result")
def a(b):
    return b * 2


print(a(78))
print(repeat("uu"))
print(decorator_test(6, 9))
