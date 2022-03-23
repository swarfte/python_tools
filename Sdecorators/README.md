# python通用裝飾器 Sdecorators

## 基礎裝飾器 BaseDecorator

* ### 內置屬性

> * self.func 被裝飾的函數
>* self.func_args 被裝飾函數的可變位置參數
>* self.func_kwargs 被裝飾函數的關鍵字參數
>* self.func_result 被裝飾函數運行後的返回值
>* self.decorator_args 對像裝飾器自身的可變位置參數
>* self.decorator_kwargs 對像裝飾器自身的關鍵字參數

* ### 內置函數(interface)

> * before_invoke() 被裝飾函數運行前的工作
>* invoke() 調用被裝飾的函數
>* after_invoke() 被裝飾函數運行後的工作 (在被裝飾的函數return 前執行)

## 基於 BaseDecorator 的裝飾器

>* ### 裝飾被裝飾函數的參數 DecorateTheParameters(self, decorate_func, parameters_index: int = 0)
>* ### 裝飾被裝飾函數的回傳值 DecorateTheReturn(self, decorate_func)
>* ### 記錄被裝飾函數的調用次數,用group來劃分不同的組別 InvokeCount(self, group: str = keywords["default"])
>* ### 記錄被裝飾函數的運行時間 RunTimeMonitor(self, sentence: str = keywords["default"])
>* ### 忽略特定的異常 IgnoreException(self, exception=Exception)
>* ### 打印被裝飾函數的參數和其返回值 ShowFunctionDetail(self, sentence: str = keywords["default"])
>* ### 用於重複執行被裝飾的函數 Repeater (self, start: int = 0, end: int = 1, interval: int = 1)
>* ### 把被裝飾函數的回傳值保存至指定的json檔 JsonSaveReturn(self, config_path: str = keywords["default"], key: str = keywords["default"])
>* ### 讓被裝飾函數的參數通過json檔獲取數值,可使用篩選函數判斷是否需要替換 JsonReadData(self, config_path: str, key: str, parameters_index: int = 0, judgment_function=keywords["default"])

