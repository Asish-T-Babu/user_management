from unicodedata import name
from app1 import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('login/', views.login, name="login"),
    path('home', views.home, name="home"),
    path('insert/',views.insert,name="insert"),
    path('admin_insert/',views.admin_insert,name="admin_insert"),
    path('logout',views.logout, name='logout'),
    path('<int:id>',views.deleterow, name='delete'),
    path('update/<int:id>',views.updaterow, name='update'),
    path('user_home/', views.user_home, name="user_home"),
]
