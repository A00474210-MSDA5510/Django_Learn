from django.urls import path, include
from . import views

urlpatterns = [
    path("hello", views.home),
    path("allHotels", views.gethotels),
    path("classhotels", views.Hotel_List.as_view())
]