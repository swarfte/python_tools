import pyppeteer
import asyncio


class BaseReptile(object):  # 基本的pyppeteer爬蟲
    def __init__(self, url: str, user_agent: str = "", browser_width: int = 1920, browser_height: int = 1080):  # 初始化設國
        super(BaseReptile, self).__init__()
        self.headless = False
        self.url = url
        self.user_agent = user_agent
        self.browser = None
        self.browser_page = None
        self.browser_width = browser_width
        self.browser_height = browser_height

    async def setup(self):  # 初始化 打開瀏覽器
        self.browser = await pyppeteer.launch(headless=self.headless, args=[
            '--disable-infobars',
            '--start-maximized',
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
        ], dumpio=True)  # *創建瀏覽器
        self.browser_page = await self.browser.newPage()
        await self.browser_page.evaluate(
            """() =>{Object.defineProperties(navigator, {webdriver:{get: () => false}})}""")
        await self.browser_page.evaluate('''() => {window.navigator.chrome = {runtime: {}, }; }''')
        await self.browser_page.evaluate(
            '''() =>{Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});}''')
        await self.browser_page.evaluate(
            '''() =>{Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
        await self.browser_page.setUserAgent(self.user_agent)
        await self.browser_page.setViewport({  # *設置畫面的視窗大小
            "width": self.browser_width,
            "height": self.browser_height
        })

    async def close(self):
        await self.browser.close()

    def browser_operate(self, async_function):
        asyncio.get_event_loop().run_until_complete(async_function())

    def browser_setup(self):
        self.browser_operate(self.setup)

    def browser_close(self):
        self.browser_operate(self.close)

    async def get_page_url(self, page):
        return await page.url

    async def get_page_cookies(self, page):
        return await page.cookies()

    async def run(self):
        pass

    def browser_run(self):
        self.browser_operate(self.run)

    def __enter__(self):
        self.browser_setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser_close()
