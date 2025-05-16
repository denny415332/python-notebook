# Python 多層函式（嵌套函式）

在 Python 中，「多層函式」（也常稱作「嵌套函式」或「巢狀函式」）是指在一個函式（外函式）內部定義另一個函式（內函式）。其主要作用與優點包括：

1. **封裝與命名空間隔離**  
   - 內函式只在外函式作用域內可見，不會污染全域命名空間。  
   - 適合將只被單一函式使用的輔助程式碼隱藏起來。

2. **閉包（Closure）與狀態保存**  
   - 內函式可以「捕捉」並記住外函式的參數及局部變數，形成閉包，從而保留執行時的環境狀態。  
   - 常用於建立帶有內部狀態的函式工廠（function factory）。

3. **高階函式／裝飾器**  
   - 建立裝飾器（decorator）時，典型地透過多層函式接受被裝飾函式，然後在內層函式中包裹額外行為。

4. **實現回呼（Callback）或局部輔助**  
   - 將上下文相關的輔助函式局部化，並作為回呼傳遞。

---

## 範例 1：閉包示例（Counter 工廠）
```python
def make_counter():
    count = 0
    def counter():
        nonlocal count      # 告訴 Python 我們要修改外層 count
        count += 1
        return count
    return counter

c1 = make_counter()
print(c1())  # 1
print(c1())  # 2

c2 = make_counter()
print(c2())  # 1  （c2 保有自己獨立的 count）
```

- `make_counter()` 回傳的 `counter` 內函式，就「閉包」住了 `count` 變數。

---

## 範例 2：簡易裝飾器
```python
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"呼叫 {func.__name__}，參數：{args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 回傳：{result}")
        return result
    return wrapper

@debug
def add(a, b):
    return a + b

add(3, 5)
```

- `debug` 是外函式，`wrapper` 是內函式。`@debug` 語法下，`add` 被包在 `wrapper` 內層中，實現呼前與呼後的附加行為。

---

## 範例 3：局部輔助函式
```python
def process(data):
    def clean(x):
        # 只在 process() 中使用，不會成為全域名稱
        return x.strip().lower()
    
    return [clean(item) for item in data]

raw = [" Alice ", "Bob ", "  ChArLie"]
print(process(raw))
# ['alice', 'bob', 'charlie']
```

- `clean` 只在 `process` 函式體內有效，可防止外部誤用。

---

## 注意事項
- 若內函式要修改外層變數，必須使用 `nonlocal`（或 `global`，但盡量避免全域污染）。  
- 過度使用嵌套函式可能會讓程式結構複雜，需平衡可讀性。

透過多層函式，你可以更靈活地管理作用域、封裝狀態，並實現高階函式、閉包與裝飾器等強大功能。