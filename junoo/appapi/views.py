from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from common.func.responseTemp import basic_response as response
#from rest_framework.serializers import *
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_protect
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt

from django.db.models import Sum
import random
import datetime
import requests

from .models import *
from.serializers import *
# Create your views here.
from . serializers import *
from masters.models import *

class GetPhoneNumber(APIView):
    def post(self,request):
        code=request.data['code']
        mobile = request.data['mobile']
        return response(False, code, "")

class GetOtp(APIView):
    def post(self, request):
        code = request.data['code']
        mobile = request.data['mobile']
        otp = request.data['otp']

        res=True
        if res == True:
            status = True
            try:
                user = User.objects.get(username=mobile)
            except:
                user = None
            if user is not None:
                    try:
                        cus = Customer.objects.get(user=user.id)
                    except:
                        cus = None

                    if cus:
                        refresh = RefreshToken.for_user(user)
                        refresh['phonenumber'] = user.username
                        refresh['customer'] = cus.id
                        refresh['junoocategory_id'] = cus.junoocategory.id
                        refresh['junoosubcategory_id'] = cus.junoosubcategory.id
                        resdata = { 'already_user':True,'refresh': str(refresh), 'access': str(refresh.access_token)}
                        message="success"
                    else:
                        status = False
                        resdata = { 'already_user':False }
                        message = "Data Not Found"

            else:
                status = False
                resdata = {'already_user':False}
                message = "Data Not Found"
        else:
            status = False
            resdata=None
            message="Wrong Otp"
        return response(status, message, resdata)

class RegisterUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.data['mobile']
            country_code = serializer.data['country_code']

            a = User.objects.create(username=request.data['mobile'])
            a.save()
            created_date = date.today()

            name=request.data['name']
            junoocategory_id=request.data['junoocategory_id']
            junoosubcategory_id=request.data['junoosubcategory_id']
            c = Customer(user=a, mobile=mobile, status=True,country_code=country_code,date=created_date,name=name,junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id,)
            c.save()
            refresh = RefreshToken.for_user(a)
            refresh['phonenumber'] = a.username
            cus = Customer.objects.get(id=c.id)
            refresh['customer'] = cus.id
            refresh['junoocategory_id'] = request.data['junoocategory_id']
            refresh['junoosubcategory_id'] = request.data['junoosubcategory_id']
            res = {'already_user':True,'refresh': str(refresh), 'access': str(refresh.access_token)}
            return response(True, "Success", res)



        else:
            return response(False,"error",serializer.errors)


class JunooCats(APIView):
    def get(self, request):
        junnocatsdata = junoocategory.objects.filter(status=True)
        if junnocatsdata is not None:
            res = []
            for jc in junnocatsdata:
                subres = []
                if jc.get_junnosubcats is not None:
                    for sjc in jc.get_junnosubcats:
                        subtemps = {
                            "junoosubcatid":sjc.id,
                            "junoosubcattitle": sjc.title,
                        }
                        subres.append(subtemps)

                tempdata={
                    "junoocatid":jc.id,
                    "title":jc.title,
                    "subcats":subres
                }
                res.append(tempdata)
        else:
            res = None
        return response(True, "success", res)