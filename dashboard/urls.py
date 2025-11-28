from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('kelola_user/', views.dashboard_kelola_user, name='kelola_user'),
    path('kelola_user/edit/<int:id_user>/', views.dashboard_edit_user, name='edit_user'),
    path('kelola_user/delete/<int:id_user>/', views.dashboard_delete_user, name='delete_user'),
    path('kelola_history/', views.dashboard_kelola_history, name='kelola_history'),
    path('kelola_history/detail/<str:id_cek>/', views.dashboard_detail_history, name='detail_history'),
    path('kelola_history/delete/<str:id_cek>/', views.dashboard_delete_history, name='delete_history'),
    path('not_admin/', views.not_admin_view, name='not_admin'),
]