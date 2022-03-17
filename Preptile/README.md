# 通用pyppeteer爬蟲模型(Preptile)

## 常用函數

### (所有函數預設值使用object內的對應的屬性)

### 集成函數
>* login 用於在網頁中登入帳戶
>* xpath_data 通過xpath表達式獲取匹配的元素並返回指定的屬性
>* get_element_text 獲取第一個匹配元素的文本
>* get_all_element_text 獲取全部匹配元素的文本
>* get_element_url 獲取第一個匹配元素的連結
>* get_all_element_url 獲取全部匹配元素的連結
>* turn_pages 翻頁並執行指定函數

### 瀏覽器函數

> * newPage 開啟新的分頁
>* close_browser 關閉瀏覽器

### 瀏覽器頁面函數

> * goto 訪問指定的連結
>* content 獲取網頁的源代碼
>* evaluate 在網頁內執行js代碼並獲取結果
>* close_page 關閉瀏覽器的分頁
>* click 點擊網頁中指定的元素
>* type 在指定的元素(input等)輸入資料
>* select 在指定的元素(select等)選擇資料
>* querySelectorEval 通過css選擇器選出第一個匹配的元素後執行js代碼並獲取結果
>* querySelectorAllEval 通過css選擇器選出全部匹配的元素後執行js代碼並獲取結果
>* reload 刷新當前頁面
>* goBack 退回上一頁
>* goForward 前進下一頁
>* setUserAgent 設置頁面的用戶代理
>* title 返回網頁的標題
>* cookies 返回網頁的cookies
>* waitForSelector 等待符合選擇器的節點加載出來
>* waitForFunction 等待要執行的js代碼

### 全域函數

> * sleep 等待指令秒數

## 進階函數

> * @async_operate 用於瀏覽器操作(需要異步)的函數
>* check_default  判斷是否為默認值
>* setViewport設置頁面的可視範圍大小