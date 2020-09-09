from django.urls import path
from django01 import views

app_name = 'django01'

urlpatterns = [
    path('user/', views.user, name='user'),
    path('userView/<str:id>/', views.Userview.as_view(), name='userView')
]