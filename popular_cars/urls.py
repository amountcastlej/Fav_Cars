from django.urls import path, include

urlpatterns = [
    path('', include('cars_app.urls')),
]
