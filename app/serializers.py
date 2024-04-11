from rest_framework import serializers
from .models import Hotels
class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotels
        fields = "__all__"