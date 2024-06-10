
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home.html',views.home,name="home"),
    path('adoption.html',views.adoption,name="adoption"),
    path('advice.html',views.advice,name="advice"),
    path('pets.html',views.pets,name="pets"),
    path('shop.html',views.shop,name="shop"),
    path('login.html',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('adopted_pet/<int:pk>/', views.adopted_pet , name='adopted_pet'),
    path('search.html',views.search,name="search"),
    
]
