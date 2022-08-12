from rest_framework import serializers
from masters.models import *
# Create your models here.
from .models import *

class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=400)
    country_code = serializers.CharField(max_length=400)

    name = serializers.CharField(max_length=400)
    junoocategory_id = serializers.CharField(max_length=400)
    junoosubcategory_id = serializers.CharField(max_length=400)