from django.urls import path

from serializersapp import views

app_name='serializersapp'

urlpatterns=[
    path('empAPIView/',views.EmployeeAPIView.as_view(),name='empAPIView'),
    path('empAPIView/<str:id>/',views.EmployeeAPIView.as_view(),name='empAPIView'),
]