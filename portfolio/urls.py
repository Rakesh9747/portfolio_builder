from django.contrib import admin
from django.urls import path
from portfolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
   

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_portfolio),
    path('select-template/', views.select_template),
    path('build/', views.build_portfolio),

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('portfolio/<str:username>/', views.portfolio_view, name='portfolio_view'),
]