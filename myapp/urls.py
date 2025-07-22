from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('post/',views.posts,name="post"),
    path('message/',views.message,name="message"),
    path('chat/<str:username>/',views.chat,name="chat"),
    path('profile/<str:username>/', views.profile, name="profile"),
    

]