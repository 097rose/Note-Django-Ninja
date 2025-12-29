# Note Audit System (Django Ninja-Extra)

---

## 🚀 核心功能與實作亮點

### 1. 審計日誌
* **自動偵測變更**：當筆記更新時，系統會精確對比新舊資料，僅紀錄有變動的欄位名稱 (`changed_fields`)。
* **資料一致性**：使用 `@transaction.atomic` 確保「筆記更新」與「日誌寫入」在資料庫層級同步成功，絕不漏掉審計線索。

### 2. SSE 歷史紀錄串流
* **逐筆輸出**：利用 Python Generator (`yield`) 實作即時串流，每筆紀錄間模擬 0.5 秒處理延遲。
* **標準終止協議**：符合實務規範，在所有紀錄傳輸完成後，會發送一個 `event: end` 訊號，方便前端優化連線管理。

### 3. 分層架構設計
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
```
### 2. 資料庫初始化
```
python manage.py makemigrations notes
python manage.py migrate
```
### 3.啟動 server
```
python manage.py runserver
```

## 測試指令

### API文件
啟動後造訪：http://127.0.0.1:8000/api/docs 
|  請求方法   | 路徑  |功能|
|  ----  | ----  | ----  |
| GET  | /api/notes | 列出所有notes|
| POST | /api/notes |建立notes|
| GET  | /api/notes/{id} |列出單筆notes|
| PATCH  | /api/notes/{id} |更新note|
| DELETE  | /api/notes/{id} |刪除note|
| GET  | /api/notes/{id}/history/stream |列出歷史紀錄|



### 測試 SSE 串流
```powershell
curl.exe -N "http://127.0.0.1:8000/api/notes/{ID}/history/stream"
```
### 預期輸出範例
```
event: note_change
data: {"action": "create", "changed_fields": [], "changed_at": "...", "changed_by": "admin_user"}

event: note_change
data: {"action": "update", "changed_fields": ["title"], "changed_at": "...", "changed_by": "editor_user"}

event: end
data: Stream has successfully completed.
```

## 專案結構
```
|- my_project/
|- notes/
|   |- controllers.py # API入口及路由管理
|   |- services.py # 處理運算
|   |- schemas.py
|   |- models.py # Note 與 NoteChangeLog 資料結構
|- api.py
|- manage.py
```