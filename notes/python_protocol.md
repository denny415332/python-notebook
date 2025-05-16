# Python Protocol 使用方法及時機

以下針對 Python 中的 `Protocol` 做一個概覽，並比較它與傳統介面（Interface）或抽象基底類別（ABC）的差異與適用時機。

---

## 1. 什麼是 `Protocol`

- 來自 `typing`（Python 3.8+）或 `typing_extensions`，用以定義「結構化子型別」（structural subtyping）。  
- 實際上並不會在執行階段強制繼承，只要物件「長得像」符合 Protocol 的方法簽章，就算通過型別檢查（duck typing）。

```python
from typing import Protocol

class Serializer(Protocol):
    def serialize(self) -> str: ...
```

---

## 2. 使用時機

1. **靜態型別檢查**  
   - 想在 MyPy、Pyright 等工具中保證傳入物件含有特定方法／屬性，但不想綁定繼承關係。  
2. **減少樣板（boilerplate）**  
   - 不用每個實作類都顯式繼承自某個抽象基底，而是「隱式」符合署名即可。  
3. **多重無侵入擴充**  
   - 現有類別若未繼承自你的 ABC，也能直接被當成協定（Protocol）的實作。

---

## 3. Protocol 範例

```python
from typing import Protocol

class Serializer(Protocol):
    def serialize(self) -> str:
        ...

class JSONSerializer:
    def __init__(self, data: dict):
        self.data = data

    def serialize(self) -> str:
        import json
        return json.dumps(self.data)

def save(obj: Serializer) -> None:
    # 只要 obj 有 serialize() → 當參數就可以
    content = obj.serialize()
    print("Saved:", content)

js = JSONSerializer({"a": 1, "b": 2})
save(js)      # ✅ 通過型別檢查，也能正常執行
```

---

## 4. `Protocol` vs. `ABC`

| 特性        | Protocol                      | ABC（`abc.ABC`）            |
|-------------|-------------------------------|-----------------------------|
| 型別檢查    | 結構化（只要符號即通過）      | 名義（必須繼承才通過）      |
| 執行期檢查  | 預設無                         | 預設強制（無實作就無法實例化） |
| 樣板量      | 少（不需繼承）                 | 多（必須繼承並實作抽象方法） |
| 版本需求    | Python 3.8+ 或安裝 typing_extensions | Python 標準皆可              |

---

## 5. 是否「有必要」使用 Protocol？

- **不是必要**，只是一種「開發期型別輔助」工具。  
- 若你的程式以動態型別為主，且不使用靜態檢查工具，也可以直接利用 Python 的 duck typing。不繼承任何介面，只要呼叫時有該方法就行。  
- 如果團隊有採用 MyPy 等靜態檢查，又希望對參數「介面契約」做明確註解，那 Protocol 能讓程式碼更清晰、檢查更嚴謹。

---

### 小結

1. **只需註解、靜態檢查 →** 優先考慮 `Protocol`  
2. **需執行期強制、嚴格繼承 →** 考慮 `abc.ABC`  
3. **不需要型別檢查 →** 直接使用 duck typing，即可達到最輕量的「介面」效果。  
