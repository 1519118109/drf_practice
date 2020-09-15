from django.urls import path

from modelapp import views

app_name='modelapp'

urlpatterns=[
    path('bookAPIView/', views.BookAPIView.as_view(), name='bookAPIView'),
    path('bookAPIView/<str:id>/', views.BookAPIView.as_view(), name='bookAPIView'),
    path('bookAPIViewV2/', views.BookAPIViewV2.as_view(), name='bookAPIViewV2'),
    path('bookAPIViewV2/<str:id>/', views.BookAPIViewV2.as_view(), name='bookAPIViewV2'),
]