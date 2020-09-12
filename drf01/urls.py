from django.urls import path

from drf01 import views

app_name= 'drf01'

urlpatterns=[
    path('userAPIView/', views.UserAPIView.as_view(), name='userAPIView'),
    path('userAPIView/<str:id>/', views.UserAPIView.as_view(), name='userAPIView'),
    path('studentAPIView/', views.StudentAPIView.as_view(), name='studentAPIView'),
    path('studentAPIView/<str:id>/', views.StudentAPIView.as_view(), name='studentAPIView'),


]