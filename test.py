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
    for x in range(2, 5):
        print(decorator_test(x, 5))
    with TestReptile(
            "https://www.google.com/search?q=google&oq=google&aqs=edge..69i57j0i20i263i433i512l2j0i67i433j69i59j0i67i433j69i60l3.2005j0j1&sourceid=chrome&ie=UTF-8",
            ) as Connector:
        Connector.browser_run()
