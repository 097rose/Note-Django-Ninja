import uuid
from django.db import models

class Note(models.Model):
    # 使用 UUID 作為 ID (題目建議)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # 完整審計欄位 (Requirement 1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class NoteChangeLog(models.Model):
    # 關聯到 Note
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='changelogs')
    
    # 修改資訊 (Requirement 3)
    action = models.CharField(max_length=20)  # create, update, delete
    changed_fields = models.JSONField(default=list)  # 記錄哪些欄位變了
    
    # 記錄變更前與變更後的狀態
    before_state = models.JSONField(null=True, blank=True)
    after_state = models.JSONField(null=True, blank=True)
    
    changed_by = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at'] # 最新的紀錄排在前面