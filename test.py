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
    @reptile.browser_operate
    async def search(self):
        await self.browser_page.goto(self.url)
        await asyncio.sleep(2)

    def run(self):
        self.search()


if __name__ == "__main__":
    with TestReptile("http://www.vakiodigital.com/login") as Connector:
        Connector.run()
