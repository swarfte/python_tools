import Sdecorators
import Preptile as reptile
import asyncio


@Sdecorators.IgnoreException()
@Sdecorators.RunTimeMonitor()
@Sdecorators.InvokeCount()
@Sdecorators.ShowFunctionDetail()
@Sdecorators.ConvertResultType(str)
def decorator_test(a, b):
    print('starting')

    return a * b


class TestReptile(reptile.BaseReptile):
    pass


with reptile.BaseReptile("http://www.vakiodigital.com/login") as Connector:
    Connector.goto()
