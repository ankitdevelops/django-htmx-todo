from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('check-user/', views.check_user, name='check-user'),
    path('email-check', views.email_check, name='email-check'),
    path('add-todo', views.add_todo, name='add-todo'),
    path('mark-complete/<int:id>/', views.mark_complete, name='mark-complete'),
    path('delete-todo/<int:id>/', views.delete_todo, name='delete-todo'),

]
