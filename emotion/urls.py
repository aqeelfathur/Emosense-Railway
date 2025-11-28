from django.urls import path
from . import views

app_name = 'emotion'

urlpatterns = [
    path('', views.cek_emosi, name='cek_emosi'),
    path('analyze-youtube/', views.analyze_youtube, name='analyze_youtube'),
]