import datetime as dt
import functools
import json
import os

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

    def run(self, func):  # 運行裝飾器函數
        """Run the decorator function"""

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


class DecorateTheParameters(BaseDecorator):  # 裝飾被裝飾函數的參數
    """Decorate the parameters of the decorated function"""

    def __init__(self, decorate_func, parameters_index: int = 0):  # 傳入要裝飾被裝飾函數形參的函數
        super(DecorateTheParameters, self).__init__()
        self.decorate_func = decorate_func
        self.parameters_index = parameters_index

    def before_invoke(self):
        self.func_args = list(self.func_args)
        self.func_args[self.parameters_index] = self.decorate_func(self.func_args[self.parameters_index])
        self.func_args = tuple(self.func_args)
        # self.func_args = tuple([self.decorate_func(x) for x in self.func_args])
        # for k, y in self.func_kwargs.items():
        #     self.func_kwargs[k] = self.decorate_func(y)


class DecorateTheReturn(BaseDecorator):  # 裝飾被裝飾函數的回傳值
    """Change the return type of the decorated function"""

    def __init__(self, decorate_func):  # 傳入要裝飾被裝飾函數回傳值的函數
        super(DecorateTheReturn, self).__init__()
        self.decorate_func = decorate_func

    def after_invoke(self):
        self.func_result = self.decorate_func(self.func_result)


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

    def count(self) -> int:  # 對被裝飾函數的調用次數進行計數
        """Count the number of times the decorated function is called"""
        if self.group in InvokeCount.number.keys():
            InvokeCount.number[self.group] += 1
        else:
            InvokeCount.number[self.group] = 1
        return InvokeCount.number[self.group]

    def after_invoke(self):
        self.show_result()

    def show_result(self):  # 顯示被裝飾函數調用的次數
        """Displays the number of times the decorated function is called"""
        print(f'{self.group} : {self.count()}')


class RunTimeMonitor(BaseDecorator):
    """Record the running time of the decorated function"""

    def __init__(self, sentence: str = keywords["default"]):
        super(RunTimeMonitor, self).__init__()
        self.sentence = str(sentence)  # 要表達函式
        self.start_time = None  # 開始運行的時間
        self.end_time = None  # 結束運行的時間
        self.run_time = 0  # 記錄被裝飾函數運行的時間

    def start_count_time(self):  # 調用被裝飾函數並開始計時
        """Call the decorated function and start timing"""
        self.start_time = dt.datetime.now().strftime("%H:%M:%S.%f")
        self.run_time = int(self.start_time[0:2]) * 3600 + int(self.start_time[3:5]) * 60 + int(
            self.start_time[6:8]) + float(self.start_time[9:11]) / 1000

    def show_start_time(self):  # 展示被裝飾函數的開始時間
        """Displays the start time of the decorated function"""
        print(f'{self.sentence} start time: {self.start_time}')

    def before_invoke(self):
        self.start_count_time()
        if self.sentence == keywords["default"]:
            self.sentence = self.func.__name__
        self.show_start_time()

    def stop_count_time(self):  # 被調用函數結束時停止計時
        """Stop timing when the called function finishes"""
        self.end_time = dt.datetime.now().strftime("%H:%M:%S.%f")
        end_run_time = int(self.end_time[0:2]) * 3600 + int(self.end_time[3:5]) * 60 + int(
            self.end_time[6:8]) + float(self.end_time[9:11]) / 1000
        self.run_time = end_run_time - self.run_time

    def show_stop_time(self):  # 展示被裝飾函數的結束時間
        """Display the end time of the decorated function"""
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

    def show_function_parameter(self):  # 展示被裝飾函數的參數
        """Display the parameters of the decorated function"""
        print(f"{self.sentence}: args -> {self.func_args} kwargs-> {self.func_kwargs}")

    def before_invoke(self):
        if self.sentence == keywords["default"]:
            self.sentence = self.func.__name__
        self.show_function_parameter()

    def show_function_result(self):  # 展示被裝飾函數的回傳值
        """Displays the return value of the decorated function"""
        print(f"{self.sentence} : result -> {self.func_result} ")

    def after_invoke(self):
        self.show_function_result()


class Repeater(BaseDecorator):  # 用於重複執行被裝飾的函數
    """Used to repeatedly execute the decorated function"""

    def __init__(self, start: int = 0, end: int = 1, interval: int = 1):
        super(Repeater, self).__init__()
        self.start = start
        self.end = end
        self.interval = interval
        self.run_time = 0  # 當前的重覆次數
        self.check()

    def check(self):  # 模擬range函數的模式
        """Modes for simulating the range function"""
        if self.start > self.end and self.interval > 0:
            self.end = self.start
            self.start = 0

    def invoke(self):
        for run in range(self.start, self.end, self.interval):
            self.run_time = run
            self.before_loop()
            self.func_result = self.func(*self.func_args, **self.func_kwargs)
            self.after_loop()

    def before_loop(self):  # 在for迴圈中執行被裝飾函數前的工作
        """Execute the work before the decorated function in the for loop"""
        pass

    def after_loop(self):  # 在for迴圈中執行被裝飾函數後的工作
        """Execute the work after the decorated function in the for loop"""
        pass


class JsonSaveReturn(BaseDecorator):  # 把被裝飾函數的回傳值保存至指定的json檔
    """Save the return value of the decorated function to the specified json file """

    def __init__(self, config_path: str = keywords["default"], key: str = keywords["default"]):
        super(JsonSaveReturn, self).__init__()
        self.config_path = config_path
        self.config = None
        self.key = key

    def before_invoke(self):
        if self.config_path == keywords["default"]:
            self.config_path = f"{self.func.__name__}.json"
        if self.key == keywords["default"]:
            self.key = f"{self.func.__name__}_result"
        self.check_json_path()
        self.read_json()

    def after_invoke(self):
        if self.key not in self.config:
            self.config[self.key] = []
        self.config[self.key].append(self.func_result)
        self.write_json()

    def check_json_path(self):  # 檢測路徑是否存在 如果不存在則創建全新的json檔
        """Check if the path exists, if not, create a new json file """
        if not os.path.exists(self.config_path):
            with open(self.config_path, "a", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)

    def read_json(self):  # 讀取json檔資料
        """Read json file data """
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def write_json(self):  # 寫入json檔
        """write json file """
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)


class JsonReadData(BaseDecorator):  # 讓被裝飾函數的參數通過json檔獲取數值,可使用篩選函數判斷是否需要替換
    """Let the parameters of the decorated function get the value through the json file """

    def __init__(self, config_path: str, key: str, parameters_index: int = 0,
                 judgment_function=keywords["default"]):
        super(JsonReadData, self).__init__()
        self.config_path = config_path
        self.config = None
        self.key = key
        self.parameters_index = parameters_index
        self.judgment_function = judgment_function

    def before_invoke(self):
        if not self.judgment_function == keywords["default"]:
            if not self.judgment_function(self.func_args[self.parameters_index]):  # 不滿足篩選條件則用Json數值代替
                self.read_json()
                self.assign_value()
        else:  # 預設的情況
            self.read_json()
            self.assign_value()

    def read_json(self):  # 讀取json檔資料
        """Read json file data """
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def assign_value(self):  # 傳入json檔的數值取代被裝飾函數的參數
        """The value passed in the json file replaces the parameter of the decorated function  """
        self.func_args = list(self.func_args)
        self.func_args[self.parameters_index] = self.config[self.key]
