# Note Audit System (Django Ninja-Extra)

這是一個基於 **Django 6.0** 與 **Django Ninja-Extra** 實作的筆記管理與審計系統。本專案嚴格遵循 **Service/Controller 分層架構**，並實作了即時的 **SSE (Server-Sent Events) 歷史紀錄串流**。

---

## 🚀 核心功能與實作亮點

### 1. 審計日誌 (Requirement 3)
* **自動偵測變更**：當筆記更新時，系統會精確對比新舊資料，僅紀錄有變動的欄位名稱 (`changed_fields`)。
* **資料一致性**：使用 `@transaction.atomic` 確保「筆記更新」與「日誌寫入」在資料庫層級同步成功，絕不漏掉審計線索。

### 2. SSE 歷史紀錄串流 (Requirement 4)
* **逐筆輸出**：利用 Python Generator (`yield`) 實作即時串流，每筆紀錄間模擬 0.5 秒處理延遲。
* **標準終止協議**：符合實務規範，在所有紀錄傳輸完成後，會發送一個 `event: end` 訊號，方便前端優化連線管理。

### 3. 分層架構設計 (Requirement B)
* **Controller**：負責 HTTP 請求處理、輸入驗證 (Schema Validation) 與回應狀態碼管理 (201/204/404 等)。
* **Service**：封裝核心商業邏輯、複雜的 Diff 計算與資料庫事務處理。

---

## 🛠️ 環境架設與啟動

### 1. 安裝環境
```powershell
# 建立虛擬環境
python -m venv .venv_note

# 啟動環境 (Windows)
.\.venv_note\Scripts\activate

# 安裝依賴套件
pip install -r requirements.txt