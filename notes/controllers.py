from django.http import StreamingHttpResponse
from ninja_extra import ControllerBase, api_controller, http_get, http_post, http_patch, http_delete
from .schemas import NoteCreateIn, NoteUpdateIn, NoteOut
from .services import NoteService

@api_controller('/notes', tags=['Notes'])
class NoteController(ControllerBase):
    def __init__(self, note_service: NoteService):
        # 這裡會自動注入我們寫好的 Service
        self.service = note_service

    @http_post('', response={201: NoteOut})
    def create_note(self, data: NoteCreateIn):
        # 題目要求：使用者來源可簡化 (mock user)
        user = "admin_user"
        return self.service.create_note(data.dict(), user)

    @http_get('', response=list[NoteOut])
    def list_notes(self, limit: int = 10, offset: int = 0):
        # 題目要求：支援分頁
        from .models import Note
        return Note.objects.all()[offset : offset + limit]

    @http_get('/{id}', response=NoteOut)
    def get_note(self, id: str):
        from .models import Note
        from django.shortcuts import get_object_or_404
        return get_object_or_404(Note, id=id)

    @http_patch('/{id}', response=NoteOut)
    def update_note(self, id: str, data: NoteUpdateIn):
        user = "editor_user"
        # 排除未傳入的欄位 (exclude_unset=True)
        return self.service.update_note(id, data.dict(exclude_unset=True), user)

    @http_delete('/{id}', response={204: None})
    def delete_note(self, id: str):
        user = "admin_user"
        self.service.delete_note(id, user)
        return 204, None

    # SSE Streaming API (要求 4)
    @http_get('/{id}/history/stream')
    def stream_note_history(self, id: str):
        """
        串流回傳修改歷史
        """
        # 呼叫 Service 層提供的 Generator
        generator = self.service.get_sse_history(id)
        
        # 回傳 StreamingHttpResponse，並設置正確的 Header
        return StreamingHttpResponse(
            generator, 
            content_type='text/event-stream'
        )