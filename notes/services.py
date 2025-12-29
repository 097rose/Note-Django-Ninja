import time
import json
from typing import Iterable, Any
from django.db import transaction
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from .models import Note, NoteChangeLog

class NoteService:
    @transaction.atomic
    def create_note(self, data: dict, user: str) -> Note:
        # 1. 建立 Note 實例
        note = Note.objects.create(
            title=data['title'],
            content=data['content'],
            created_by=user,
            updated_by=user
        )
        # 2. 紀錄初始 Log
        NoteChangeLog.objects.create(
            note=note,
            action="create",
            after_state=model_to_dict(note),
            changed_by=user
        )
        return note

    @transaction.atomic
    def update_note(self, note_id: str, data: dict, user: str) -> Note:
        note = get_object_or_404(Note, id=note_id)
        before_state = model_to_dict(note)
        
        # 3. 計算哪些欄位真的變了 (符合要求 3 的 changed_fields)
        changed_fields = []
        for key, value in data.items():
            if getattr(note, key) != value:
                setattr(note, key, value)
                changed_fields.append(key)
        
        if changed_fields:
            note.updated_by = user
            note.save()
            # 4. 紀錄修改 Log
            NoteChangeLog.objects.create(
                note=note,
                action="update",
                changed_fields=changed_fields,
                before_state=before_state,
                after_state=model_to_dict(note),
                changed_by=user
            )
        return note

    def delete_note(self, note_id: str, user: str):
        note = get_object_or_404(Note, id=note_id)
        # 紀錄刪除前狀態
        NoteChangeLog.objects.create(
            note=note,
            action="delete",
            before_state=model_to_dict(note),
            changed_by=user
        )
        note.delete()

    def get_sse_history(self, note_id: str) -> Iterable[str]:
        """
        SSE Generator (符合要求 4)
        """
        logs = NoteChangeLog.objects.filter(note_id=note_id).order_by('changed_at')
        
        for log in logs:
            # 模擬延遲（要求：0.2~1s）
            time.sleep(0.5)
            
            # 構建 SSE 格式資料
            data = {
                "action": log.action,
                "changed_fields": log.changed_fields,
                "changed_at": log.changed_at.isoformat(),
                "changed_by": log.changed_by
            }
            # 必須符合 event: ... \n data: ... \n\n 格式
            yield f"event: note_change\ndata: {json.dumps(data)}\n\n"
        yield "event: end\ndata: Stream has successfully completed.\n\n"