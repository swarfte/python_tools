import pyppeteer
import asyncio
import functools

default = "self"


def check_default(func_var, object_var):  # 判斷是否為預設值
    """Determine whether it is the default value"""
    if func_var == default:
        return object_var
    else:
        return func_var


def async_operate(async_function):  # 用於處理瀏覽器的異步操作
    """Asynchronous operations for handling browsers"""

    @functools.wraps(async_function)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(async_function(*args, **kwargs))

    return wrapper


class BaseReptile(object):  # 基本的pyppeteer爬蟲模型
    """Basic pyppeteer crawler model"""

    def __init__(self, url: str, user_agent: str = "", browser_width: int = 1920, browser_height: int = 1080):  #
        """Initialize settings"""
        super(BaseReptile, self).__init__()
        self.headless = False
        self.url = url
        self.user_agent = user_agent
        self.delay = 1
        self.browser = None
        self.browser_page = None
        self.browser_width = browser_width
        self.browser_height = browser_height
        self.browser_args = [
            '--disable-infobars',
            '--start-maximized',
            '--disable-extensions',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--mute-audio',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
        ]

    @async_operate
    async def setup(self):  # 初始化 打開瀏覽器
        """Initialize Open browser"""
        self.browser = await pyppeteer.launch(headless=self.headless, args=self.browser_args, dumpio=True)  # *創建瀏覽器
        self.browser_page = await self.browser.newPage()
        await self.browser_page.evaluate(
            """() =>{Object.defineProperties(navigator, {webdriver:{get: () => false}})}""")
        await self.browser_page.evaluate('''() => {window.navigator.chrome = {runtime: {}, }; }''')
        await self.browser_page.evaluate(
            '''() =>{Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});}''')
        await self.browser_page.evaluate(
            '''() =>{Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
        await self.browser_page.setUserAgent(self.user_agent)

    @async_operate
    async def setViewport(self, width: int = 1920, height: int = 1080,
                          page: pyppeteer = default) -> None:  # 設置頁面的可視範圍大小
        """Set the size of the visible range of the page"""
        await check_default(page, self.browser_page).setViewport({
            "width": width,
            "height": height
        })

    def run(self):  # 運行主程式
        """run main program"""
        pass

    def before_setup(self):  # 初始化前的工作
        """work before initialization"""
        pass

    def before_close(self):  # 關閉瀏覽器前的工作
        """Work before closing the browser"""
        pass

    def after_setup(self):  # 初始化後的工作
        """work after initialization"""
        pass

    def after_close(self):  # 關閉瀏覽器後的工作
        """Works after closing the browser"""
        pass

    def __enter__(self):  # 進入with 語句
        """into the with statement"""
        self.before_setup()
        self.setup()
        self.setViewport()
        self.after_setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # 離開with語句
        """leave the with statement"""
        self.before_close()
        self.close_browser()
        self.after_close()

    # ==============================以上是爬蟲的核心====================================================

    # ===============================以下是Preptile爬蟲的懶人函數===================================================

    @async_operate
    async def goto(self, url: str = default, page: pyppeteer = default) -> None:  # 通過鏈結訪問指定網站
        """Visit the designated website through a link"""
        await check_default(page, self.browser_page).goto(check_default(url, self.url))

    @async_operate
    async def sleep(self, time: int = default) -> None:  # 等待指定時間
        """wait for a specified time"""
        await asyncio.sleep(check_default(time, self.delay))

    @async_operate
    async def content(self, page: pyppeteer = default) -> str:  # 返回網頁的源代碼
        """Returns the source code of the web page"""
        return await check_default(page, self.browser_page).content()

    @async_operate
    async def newPage(self, browser: pyppeteer = default) -> pyppeteer:  # 開啟新的分頁
        """Open a new tab"""
        return await check_default(browser, self.browser).newPage()

    @async_operate
    async def evaluate(self, expression: str, page: pyppeteer = default) -> object:  # 在網頁內執行js代碼並獲取結果
        """Execute js code inside webpage and get result"""
        return await check_default(page, self.browser_page).evaluate(expression)

    @async_operate
    async def close_page(self, page: pyppeteer = default) -> None:  # 關閉瀏覽器的分頁
        """Turn off browser pagination"""
        await check_default(page, self.browser_page).close()

    @async_operate
    async def close_browser(self, browser: pyppeteer = default) -> None:  # 關閉瀏覽器
        """close the browser"""
        await check_default(browser, self.browser).close()

    @async_operate
    async def click(self, expression: str, page: pyppeteer = default) -> None:  # 點擊網頁中指定的元素
        """Click on the specified element in the web page"""
        await check_default(page, self.browser_page).click(expression)

    @async_operate
    async def type(self, expression: str, value: str, page: pyppeteer = default) -> None:  # 在指定的元素(<input>等)輸入資料
        """Enter data in the specified element (<input>, etc.)"""
        await check_default(page, self.browser_page).type(expression, value)

    @async_operate
    async def select(self, expression: str, value: str, page: pyppeteer = default) -> None:  # 在特定的元素(<select>等)選擇資料
        """Select data in a specific element (<select>, etc.)"""
        await check_default(page, self.browser_page).select(expression, value)

    @async_operate
    async def querySelectorEval(self, element_expression: str, js_expression: str,
                                page: pyppeteer = default) -> str:  # 通過 css 選擇器選出匹配的元素後執行js代碼並獲取結果
        """Execute the js code and get the result after selecting the matching element through the css selector"""
        return await check_default(page, self.browser_page).querySelectorEval(element_expression, js_expression)

    @async_operate
    async def querySelectorAllEval(self, element_expression: str, js_expression: str,
                                   page: pyppeteer = default) -> list:  # 通過 css 選擇器選出全部匹配的元素後執行js代碼並獲取結果
        """After selecting all matching elements through the css selector, execute the js code and get the result"""
        return await check_default(page, self.browser_page).querySelectorAllEval(element_expression, js_expression)
