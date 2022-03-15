# 通用pyppeteer爬蟲模型(Preptile)

## 常用函數

### (默認使用object內的屬性)

### 瀏覽器函數

> * newPage(self, browser) -> pyppeteer 開啟新的分頁
>* close_browser(self, browser) -> None 關閉瀏覽器

### 瀏覽器頁面函數

> * goto(self, url, page) -> None 訪問指定的連結
>* content(self, page) -> str 獲取網頁的源代碼
>* evaluate(self, expression,page) -> object 在網頁內執行js代碼並獲取結果
>* close_page(self, page) -> None 關閉瀏覽器的分頁
>* click(self, expression, page) -> None 點擊網頁中指定的元素
>* type(self, expression, page) -> None: 在指定的元素(input等)輸入資料
>* select(self, expression, page) -> None: 在指定的元素(select等)選擇資料
>* querySelectorEval(self, element_expression, js_expression, page) -> str 通過 css 選擇器選出匹配的元素後執行js代碼並獲取結果
>* querySelectorAllEval(self, element_expression, js_expression, page) -> list 通過 css 選擇器選出全部匹配的元素後執行js代碼並獲取結果

### 全域函數

> * sleep(self,time) -> None 等待指令秒數

## 進階函數

> * @async_operate 用於瀏覽器操作(需要異步)的函數
>* check_default(func_var, object_var)  判斷是否為默認值
>* setViewport(self, width, height, page)設置頁面的可視範圍大小