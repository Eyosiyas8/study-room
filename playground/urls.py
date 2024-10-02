from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name='home'),

    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),

    path('create-user', views.createUser, name='create-user'),
    path('delete-chat/<str:pk>/', views.deleteChat, name='delete-chat'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('update-user/', views.updateUser, name='update-user'),
    path('update-chat/<str:pk>/', views.updateChat, name='update-chat'),

    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('chat/<str:username>/', views.chat, name='chat'),
    
    # path('delete-recent/<str:pk>/', views.deleteRecent, name='delete-recent'),
    # path('add-message', views.createMessage, name='add-message'),
    # path('update-message/<str:pk>/', views.updateMessage, name='update-message')
]