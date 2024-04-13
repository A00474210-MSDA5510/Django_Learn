from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Hotels
from .serializers import HotelSerializers
from rest_framework import generics, filters
import json
import hashlib
import base64
# Create your views here.

def home(request):
    return HttpResponse("<h1>Giggity<h1>")



def verify_post_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Check for presence of all required keys
            required_keys = ['hotel_name', 'checkin', 'checkout', 'guests_list']
            if all(key in data for key in required_keys):
                # Check for non-empty strings and list
                if (isinstance(data['hotel_name'], str) and data['hotel_name'].strip() and
                    isinstance(data['checkin'], str) and data['checkin'].strip() and
                    isinstance(data['checkout'], str) and data['checkout'].strip() and
                    isinstance(data['guests_list'], list)):

                    if not data['guests_list']:
                        return JsonResponse({'error': 'Guests list cannot be empty'})

                    for guest in data['guests_list']:
                        if 'guest_name' in guest and 'gender' in guest:
                            if not (isinstance(guest['guest_name'], str) and guest['guest_name'].strip() and
                                    isinstance(guest['gender'], str) and guest['gender'].strip()):
                                return JsonResponse({'error': 'Invalid data format for guest_name or gender'})
                        else:
                            return JsonResponse({'error': 'Missing guest_name or gender in guests_list'})

                    # If all checks pass, compute and return the MD5 hash of the JSON string
                    json_string = json.dumps(data, sort_keys=True)  # Sort keys for consistent hashing
                    hash_md5 = hashlib.md5(json_string.encode('utf-8')).hexdigest()
                    confirmation_code = base64.b64encode(hash_md5.encode('utf-8')).decode('utf-8')
                    return JsonResponse({'hash': confirmation_code})
                else:
                    return JsonResponse({'error': 'Invalid data format or empty fields'})
            else:
                return JsonResponse({'error': 'Missing hotel_name, checkin, checkout, or guests_list'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

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
        else:
            return Response({"Message": "Add Failed"})

@api_view(["POST"])
def hotel_response(request):
    if request.method == 'POST':
        response = verify_post_data(request)
        return response
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})






class Hotel_List(generics.ListCreateAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelSerializers

    filter_backends = [filters.SearchFilter]
    search_fields = ['id']