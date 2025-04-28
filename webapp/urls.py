from django.urls import path, include

from . import views
urlpatterns = [
    path ('', views.home_page, name="home"),
    path ('sting/', views.chatbot_page, name="chatbot"),
    path ('dashboard/', views.dashboard_page, name="dashboard"),
    path ('userHome/', views.userHomePage, name="userHome"),
    path('addUser',views.userAdd),
    path('dologin',views.doLogin, name="dologin"),
    path('logout',views.doLogout, name="logout"),
    path('getUser/<int:userId>',views.getUser),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('base/', views.user_list, name='base'),
    path('base/users/', views.user_list, name='user_list'),
    path('base/users/add/', views.user_add, name='user_add'),
    path('base/users/edit/<int:id>/', views.user_edit, name='user_edit'),
    path('base/users/delete/<int:id>/', views.user_delete, name='user_delete'),
    path('addReview',views.userReview),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.review_create, name='review_add'),
    path('reviews/edit/<int:pk>/', views.review_update, name='review_edit'),
    path('reviews/delete/<int:pk>/', views.review_delete, name='review_delete'),
 
]


	
   
   

   
   
  
   
   
   



    