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


class TestDecorator(Sdecorators.Repeater):
    def before_loop(self):
        print("loop start")
        print(f'run time : {self.run_time}')


@TestDecorator(1,6,2)
def repeat():
    print("repeat !!")


repeat()
