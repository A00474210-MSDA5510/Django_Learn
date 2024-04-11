from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Hotels
from .serializers import HotelSerializers
from rest_framework import generics, filters
# Create your views here.

def home(request):
    return HttpResponse("<h1>Giggity<h1>")

@api_view(["GET","POST"])
def gethotels(request):
    if request.method == "GET":
        hotels_list = Hotels.objects.all()
        hotelSerializer = HotelSerializers(hotels_list, many=True)
        return Response(hotelSerializer.data)

    if request.method == "POST":
        request_data = request.data
        serialize_request_data = HotelSerializers(data=request_data)
        if serialize_request_data.is_valid():
            serialize_request_data.save()
        return Response({"Message": "Add Successfully"})

class Hotel_List(generics.ListCreateAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelSerializers

    filter_backends = [filters.SearchFilter]
    search_fields = ['id']