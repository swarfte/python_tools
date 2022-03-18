import datetime as dt
import functools

keywords = {
    "default": "decorated function name"
}


class BaseDecorator(object):  # 裝飾函數的裝飾器
    """ Basic decorators are used to extend other functions  """

    def __init__(self, *args, **kwargs):  # 獲取裝飾器初始化的傳入參數
        super(BaseDecorator, self).__init__()
        self.func = None  # 所裝飾的函數
        self.func_args = None  # 被裝飾函數的可變位置參數
        self.func_kwargs = None  # 被裝飾函數的關鍵字參數
        self.func_result = None  # 被裝飾函數運行後的返回值
        self.types = args  # 對像裝飾器自身的可變位置參數
        self.decorator_kwargs = kwargs  # 對像裝飾器自身的關鍵字參數

    def __call__(self, func):  # 當作函數比調用時接收的參數(接收函數作為參數->裝飾器)
        self.func = func
        return self.run(self.func)

    def run(self, func):  # 調用被裝飾函數
        @functools.wraps(func)  # 保留被裝飾函數的屬性
        def wrapper(*args, **kwargs):  # 對被裝飾函數修改/增加額外的功能
            """the decorator main control function """
            self.initialize(args, kwargs)
            self.before_invoke()
            self.invoke()
            self.after_invoke()
            return self.func_result

        return wrapper

    def initialize(self, args, kwargs):  # 裝飾器函數運行前的初始化工作
        """Initialization work before the decorator function runs"""
        self.func_args = args
        self.func_kwargs = kwargs

    def before_invoke(self):  # 被裝飾函數運行前的工作
        """Work before the decorated function runs"""
        pass

    def invoke(self):  # 調用被裝飾的函數
        """Call the decorated function """
        self.func_result = self.func(*self.func_args, **self.func_kwargs)
        pass

    def after_invoke(self):  # 被裝飾函數運行後的工作 (在被裝飾的函數return 前執行)
        """Work after the decorated function runs"""
        pass


class ConvertParameterType(BaseDecorator):  # 用於轉換被裝飾函數的形參類型
    """Change the parameter type of the decorated function """

    def __init__(self, types: type):  # 傳入讓被裝飾函數形參要轉換的類型
        super(ConvertParameterType, self).__init__()
        self.types = types

    def before_invoke(self):
        self.func_args = tuple([self.types(x) for x in self.func_args])
        for k, y in self.func_kwargs.items():
            self.func_kwargs[k] = self.types(y)


class ConvertResultType(BaseDecorator):  # 用於轉換被裝飾函數返回值的類型
    """Change the return type of the decorated function"""

    def __init__(self, types: type):  # 傳入讓返回值轉換的類型
        super(ConvertResultType, self).__init__()
        self.types = types

    def after_invoke(self):
        self.func_result = self.types(self.func_result)


class InvokeCount(BaseDecorator):  # 記錄被裝飾函數的調用次數,用group來劃分不同的組別
    """Record the number of times the decorated function is called, use the group variable to distinguish the count
    number """
    number = dict()  # class的靜態變量 和所有物件共用的變量

    def __init__(self, group: str = keywords["default"]):
        super(InvokeCount, self).__init__()
        self.group = group  # 設定分組

    def before_invoke(self):
        if self.group == keywords["default"]:
            self.group = self.func.__name__

    def count(self) -> int:  # 進行計數
        if self.group in InvokeCount.number.keys():
            InvokeCount.number[self.group] += 1
        else:
            InvokeCount.number[self.group] = 1
        return InvokeCount.number[self.group]

    def after_invoke(self):
        self.show_result()

    def show_result(self):  # 打印結果
        print(f'{self.group} : {self.count()}')


class RunTimeMonitor(BaseDecorator):
    """Record the running time of the decorated function"""

    def __init__(self, sentence: str = keywords["default"]):
        super(RunTimeMonitor, self).__init__()
        self.sentence = str(sentence)  # 要表達函式
        self.start_time = None  # 開始運行的時間
        self.end_time = None  # 結束運行的時間
        self.run_time = 0  # 記錄被裝飾函數運行的時間

    def start_count_time(self):  # 開始計時
        self.start_time = dt.datetime.now().strftime("%H:%M:%S.%f")
        self.run_time = int(self.start_time[0:2]) * 3600 + int(self.start_time[3:5]) * 60 + int(
            self.start_time[6:8]) + float(self.start_time[9:11]) / 1000

    def show_start_time(self):
        print(f'{self.sentence} start time: {self.start_time}')

    def before_invoke(self):
        self.start_count_time()
        if self.sentence == keywords["default"]:
            self.sentence = self.func.__name__
        self.show_start_time()

    def stop_count_time(self):  # 停止計時
        self.end_time = dt.datetime.now().strftime("%H:%M:%S.%f")
        end_run_time = int(self.end_time[0:2]) * 3600 + int(self.end_time[3:5]) * 60 + int(
            self.end_time[6:8]) + float(self.end_time[9:11]) / 1000
        self.run_time = end_run_time - self.run_time

    def show_stop_time(self):
        print(f'{self.sentence} cost time: {self.run_time} seconds')

    def after_invoke(self):
        self.stop_count_time()
        self.show_stop_time()


class IgnoreException(BaseDecorator):  # 忽略特定的異常
    """Ignore the specific  Exception in decorated function"""

    def __init__(self, exception=Exception):
        super(IgnoreException, self).__init__()
        self.exception = exception

    def invoke(self):
        try:
            self.func_result = self.func(*self.func_args, **self.func_kwargs)
        except self.exception as e:
            print(f'{self.func.__name__} catch "{self.exception}" : {repr(e)}')


class ShowFunctionDetail(BaseDecorator):  # 打印被裝飾函數的參數和其返回值
    """Print the parameters of the decorated function and its return value """

    def __init__(self, sentence: str = keywords["default"]):
        super(ShowFunctionDetail, self).__init__()
        self.sentence = sentence

    def show_function_parameter(self):
        print(f"{self.sentence}: args -> {self.func_args} kwargs-> {self.func_kwargs}")

    def before_invoke(self):
        if self.sentence == keywords["default"]:
            self.sentence = self.func.__name__
        self.show_function_parameter()

    def show_function_result(self):
        print(f"{self.sentence} : result -> {self.func_result} ")

    def after_invoke(self):
        self.show_function_result()
