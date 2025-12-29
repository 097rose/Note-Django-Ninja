from typing import List, Optional
from datetime import datetime
from uuid import UUID
from ninja import Schema

# 1. 建立 Note 時用的 Schema (不含 ID 和時間)
class NoteCreateIn(Schema):
    title: str
    content: str

# 2. 更新 Note 時用的 Schema (欄位皆為 Optional，支援部分更新)
class NoteUpdateIn(Schema):
    title: Optional[str] = None
    content: Optional[str] = None

# 3. 回傳單一 Note 時用的 Schema
class NoteOut(Schema):
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

# 4. SSE / 歷史紀錄回傳用的 Schema (加分項)
class NoteChangeLogOut(Schema):
    action: str
    changed_fields: List[str]
    before_state: Optional[dict]
    after_state: Optional[dict]
    changed_by: str
    changed_at: datetime