from django.urls import path

from user import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('panel/', views.panel, name='panel'),
    path('user_register', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('change_password/', views.change_password, name='user_change_password'),
    path('print/', views.print, name='print'),

]
