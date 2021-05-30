from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index), 
    path('register', views.register), 
    path('login', views.login), 
    path('cars', views.cars),
    path('add', views.add),
    path('cars/<int:car_id>', views.car),
    path('update/<int:car_id>', views.update),
    path('cars/delete/<int:car_id>', views.delete),
    path('like/<int:car_id>', views.like),
    path('user/<int:user_id>', views.user),
    path('logout', views.logout),
] 