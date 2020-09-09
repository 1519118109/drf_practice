from django.urls import path

from drf01 import views

app_name= 'drf01'

urlpatterns=[
    path('userAPIView/', views.UserAPIView.as_view(), name='userAPIView'),

]