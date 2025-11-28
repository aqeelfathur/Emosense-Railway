from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('riwayat/', views.history_list, name='history'),
    path('riwayat/detail/<str:id_cek>/', views.history_detail, name='detail'),
    path('riwayat/delete/<str:id_cek>/', views.history_delete, name='delete'),
    path('riwayat/export/', views.history_export, name='export'),
    path('riwayat/api/stats/', views.history_stats_api, name='stats_api'),
]