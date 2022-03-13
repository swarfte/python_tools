import Sdecorators
import Preptile
import asyncio


@Sdecorators.IgnoreException()
@Sdecorators.RunTimeMonitor()
@Sdecorators.InvokeCount()
@Sdecorators.ShowFunctionDetail()
@Sdecorators.ConvertResultType(str)
def decorator_test(a, b):
    print('starting')

    return a * b


class TestReptile(Preptile.BaseReptile):
    async def run(self):
        await asyncio.sleep(1)
        await self.browser_page.goto(self.url)
        await asyncio.sleep(1)



if __name__ == "__main__":
    with TestReptile("http://www.vakiodigital.com/login") as Connector:
        Connector.browser_run()
