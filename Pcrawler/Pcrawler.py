import pyppeteer
import asyncio
import functools
import collections

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


class BaseCrawler(object):  # 基本的pyppeteer爬蟲模型
    """Basic pyppeteer crawler model"""

    # region ==============================以下是爬蟲的核心====================================================
    def __init__(self, url: str, user_agent: str = "", browser_width: int = 1920,
                 browser_height: int = 1080):  # 初始化瀏覽器的設定
        """Initialize settings"""
        super(BaseCrawler, self).__init__()
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
        self.property = {
            "text": "element => element.textContent",
            "href": "element => element.href"
        }

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

    # region ===============================以下是爬蟲的基本函數===================================================

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
    async def title(self, page: pyppeteer = default) -> str:  # 返回網頁的標題
        """Returns the title of the page"""
        return await check_default(page, self.browser_page).title()

    @async_operate
    async def cookies(self, page: pyppeteer = default) -> dict:  # 返回網頁的cookies
        """"Return the cookies of the page"""
        return await check_default(page, self.browser_page).cookies()

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
                                page: pyppeteer = default) -> str:  # 通過 css 選擇器選出第一個匹配的元素後執行js代碼並獲取結果
        """Execute the js code and get the result after selecting the matching element through the css selector"""
        return await check_default(page, self.browser_page).querySelectorEval(element_expression, js_expression)

    @async_operate
    async def querySelectorAllEval(self, element_expression: str, js_expression: str,
                                   page: pyppeteer = default) -> list:  # 通過 css 選擇器選出全部匹配的元素後執行js代碼並獲取結果
        """After selecting all matching elements through the css selector, execute the js code and get the result"""
        return await check_default(page, self.browser_page).querySelectorAllEval(element_expression, js_expression)

    @async_operate
    async def reload(self, page: pyppeteer = default) -> None:  # 刷新當前頁面
        """refresh the current page"""
        await check_default(page, self.browser_page).reload()

    @async_operate
    async def goBack(self, page: pyppeteer = default) -> None:  # 退回上一頁
        """Back to previous page"""
        await check_default(page, self.browser_page).goBack()

    @async_operate
    async def goForward(self, page: pyppeteer = default) -> None:  # 前進下一頁
        """advance to next page"""
        await check_default(page, self.browser_page).goForward()

    @async_operate
    async def setUserAgent(self, user_agent: str, page: pyppeteer = default) -> None:  # 設置頁面的用戶代理
        """Set the user agent of the page"""
        await check_default(page, self.browser_page).setUserAgent(user_agent)

    @async_operate
    async def setCookie(self, cookies: dict, page: pyppeteer = default) -> None:  # 設置頁面的cookie
        """set page cookies"""
        await check_default(page, self.browser_page).setCookie(cookies)

    @async_operate
    async def waitForSelector(self, element: str, page: pyppeteer) -> None:  # 等待符合選擇器的節點加載出來
        """Wait for nodes matching the selector to load"""
        return check_default(page, self.browser_page).waitForSelector(element)

    @async_operate
    async def waitForFunction(self, js_expression: str, page: pyppeteer) -> None:  # 等待要執行的js代碼
        """Wait for the js code to be executed"""
        return check_default(page, self.browser_page).waitForFunction(js_expression)

    # region ==================================以下是爬蟲的集成函數(利用基本函數組合或複合函數)============================================

    def login(self, user_tag: str, username: str, password_tag: str, password: str, click_tag: str,
              page: pyppeteer = default) -> None:  # 用於在網頁中登入帳戶
        """Used to log in to the account on the web"""
        self.type(user_tag, username, page)
        self.type(password_tag, password, page)
        self.click(click_tag, page)

    @async_operate
    async def xpath_data(self, element_expression: str, attributes: str,
                         page: pyppeteer = default) -> str | list:  # 通過xpath表達式獲取匹配的元素並返回指定的屬性
        """Get the matched element by xpath expression and return the specified attribute"""
        elements = await check_default(page, self.browser_page).xpath(element_expression)
        if isinstance(elements, collections.Iterable):
            return [await (await x.getProperty(attributes)).jsonValue() for x in elements]
        else:
            return await(await elements.getProperty(attributes)).jsonValue()

    def get_element_text(self, element_expression: str, page: pyppeteer = default) -> str:  # 獲取第一個匹配元素的文本
        """Get the text of the first matched element """
        return self.querySelectorEval(element_expression, self.property["text"], page)

    def get_all_element_text(self, element_expression: str, page: pyppeteer = default) -> list:  # 獲取全部匹配元素的文本
        """Get the text of all matched elements """
        return self.querySelectorAllEval(element_expression, self.property["text"], page)

    def get_element_url(self, element_expression: str, page: pyppeteer = default) -> str:  # 獲取第一個匹配元素的連結
        """Get the link of the first matching element """
        return self.querySelectorEval(element_expression, self.property['href'], page)

    def get_all_element_url(self, element_expression: str, page: pyppeteer = default) -> list:  # 獲取全部匹配元素的連結
        """Get links to all matching elements """
        return self.querySelectorAllEval(element_expression, self.property['href'], page)

    def turn_pages(self, button_expression: str, non_args_func, run: int = default, delay: int = default,
                   page: pyppeteer = default) -> None:  # 翻頁並執行指定函數
        """Turn the page and execute the specified function """
        for run_time in range(check_default(run, 1)):
            non_args_func()
            self.click(button_expression, page)
            self.sleep(delay)
