from django.urls import path

from studentapp import views

app_name='studentapp'

urlpatterns=[
    path('stuAPIView/',views.StudentAPIView.as_view(),name='stuAPIView'),
    path('stuAPIView/<str:id>/',views.StudentAPIView.as_view(),name='stuAPIView'),
    path('stuAPIViewV2/', views.StudentAPIViewV2.as_view(), name='stuAPIViewV2'),
    path('stuAPIViewV2/<str:id>/', views.StudentAPIViewV2.as_view(), name='stuAPIViewV2'),
    path('stuGenericAPIView/', views.StudenetGenericMixinView.as_view(), name='stuGenericAPIView'),
    path('stuGenericAPIView/<str:id>/', views.StudenetGenericMixinView.as_view(), name='stuGenericAPIView'),
    path('stuModelViewSet/', views.StudentModelViewSet.as_view({"post":"user_login","get":"user_register"}), name='stuModelViewSet'),
    path('stuModelViewSet/<str:id>/', views.StudentModelViewSet.as_view({"post":"user_login","get":"user_register"}), name='stuModelViewSet'),
]