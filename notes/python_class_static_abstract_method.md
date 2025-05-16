# Python 教學: Class / Static / Abstract Method 初探
**最後更新時間**：2022 年 5 月 3 日

本篇講解 Python Class 類中的多種方法形式：包含 @staticmethod、 @classmethod 和 @abc.abstractmethod，建議讀者們可以一起跟著文章敲一次 code，會有更深入的了解唷。

> 本篇大綱如下：
1. StaticMethods 靜態方法：不帶實例，不帶 class 為參數的方法  
2. ClassMethods 類方法：不帶實例，帶有 class 為參數的方法  
3. AbstractMethods 抽象方法：尚未被實作，且繼承 class 一定要用覆寫來實作  

---
### Table

- [一. StaticMethods 靜態方法](#1)  
- [二. ClassMethods 類方法](#2)  
- [三. AbstractMethods 抽象方法](#3)  

<p id=1></p>

## 一. StaticMethods 靜態方法

### 使用方法
1. 在 def 函式上加上 `@staticmethod`  
2. 不用傳入 `self` 參數  

### 使用時機
- 不需要將 class 實例化即可使用函式，直接呼叫 `People_StaticMethods.work(4)`

### 範例
```python
class People_StaticMethods:
    def __init__(self):
        pass

    def sleep(self, sleep_hour):
        print('Sleeping hours :', sleep_hour)

    @staticmethod
    def work(work_hour):
        print('Working hours :', work_hour)

m = People_StaticMethods()
m.sleep(3)
People_StaticMethods.work(4)
# >>> Sleeping hours : 3
# >>> Working hours : 4
```

<p id=2></p>

## 二. ClassMethods 類方法

### 使用方法
1. 在 def 函式上加上 `@classmethod`  
2. 必須傳入 class 本身參數，通常命名為 `cls`  
3. 若要引入 class 其他函式，可使用 `cls().sleep(6)`

### 使用時機
- 不需要將 class 實例化即可使用函式，直接呼叫 `People_ClassMethods.work(5)`  
- 因為引入了 class 本身參數 `cls`，可以利用 `cls` 存取 class 內其他方法

### 範例
```python
class People_ClassMethods:
    def __init__(self):
        pass

    def sleep(self, sleep_hour):
        print('Sleeping hours :', sleep_hour)

    @classmethod
    def work(cls, work_hour):
        print('Working hours :', work_hour)
        cls().sleep(6)

People_ClassMethods.work(5)
# >>> Sleeping hours : 6
# >>> Working hours : 5
```

<p id=3></p>

## 三. AbstractMethods 抽象方法

### 使用時機
- 抽象類 (`Employee`) 不能被實例化，只能被子類繼承  
- 繼承 `Employee` 的子類必須實作 `work` 方法，否則會拋出異常  

### 範例
```python
import abc

# Python 3.4+
class Employee(abc.ABC):
    @abc.abstractmethod
    def work(self):
        return NotImplemented

class Andy(Employee):
    def work(self):
        print('work')

class Max(Employee):
    def sleep(self):
        print('sleep')

Andy().work()           # >>> work

```

### 錯誤示例
```python
Max().sleep()           # >>> TypeError: Can't instantiate abstractclass Max with abstract methods work
TypeError: Can't instantiate abstractclass Max with abstract methods work
```

### 延伸閱讀
- [[Python教學] 一切皆為物件，到底什麼是物件 Object ?](https://www.maxlist.xyz/2021/01/11/python-object/)  
- [[Python教學] 物件導向 – Class 類的 封裝 / 繼承 / 多型](https://www.maxlist.xyz/2019/12/12/python-oop/)  
- [[Python教學] Class / Static / Abstract Method 初探](https://www.maxlist.xyz/2019/12/08/python-class-static-abstract-method/)  
- [[Python教學] @property 是什麼? 使用場景和用法介紹](https://www.maxlist.xyz/2019/12/25/python-property/)  
- [[Python教學] 裝飾詞原理到應用](https://www.maxlist.xyz/2019/12/07/python-decorator/)  
- [[Python 教學] dataclass 是什麼? (python 3.7+)](https://www.maxlist.xyz/2022/04/30/python-dataclasses/)  

---

原始網頁： [Python 教學: Class / Static / Abstract Method 初探](https://www.maxlist.xyz/2019/12/08/python-class-static-abstract-method/)
