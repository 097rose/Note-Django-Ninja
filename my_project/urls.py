from django.contrib import admin
from django.urls import path
from api import api  # 引入剛才建立的 api.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls), # 所有 API 都會以 /api/ 開頭
]