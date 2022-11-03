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

from questions.models import subject


class GetOtp(APIView):
    def post(self,request):
        code=request.data['code']
        mobile = request.data['mobile']
        return response(True, code+mobile, None)

class VerifyOtp(APIView):
    def post(self, request):
        code = request.data['code']
        mobile = request.data['mobile']
        otp = request.data['otp']

        res=True
        if res == True:
            junnocatsdata = junoocategory.objects.filter(status=True)
            if junnocatsdata is not None:
                resd = []
                for jc in junnocatsdata:
                    subres = []
                    if jc.get_junnosubcats is not None:
                        for sjc in jc.get_junnosubcats:
                            subtemps = {
                                "junoosubcatid": sjc.id,
                                "junoosubcattitle": sjc.title,
                            }
                            subres.append(subtemps)

                    tempdata = {
                        "junoocatid": jc.id,
                        "title": jc.title,
                        "subcats": subres
                    }
                    resd.append(tempdata)
            else:
                resd = None
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

                        resdata = { 'already_user':True,'junoocats':resd,'refresh': str(refresh), 'access': str(refresh.access_token)}
                        message="success"
                    else:
                        status = True
                        resdata = { 'already_user':False,'junoocats':resd,}
                        message = "Data Not Found"

            else:
                status = True
                resdata = {'already_user':False,'junoocats':resd,}
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
            mobile=request.data['mobile']
            try:
                user = User.objects.get(username=mobile)
            except:
                user = None
            if user is not None:
                return response(False, "number already used", None)
            else:
                mobile = serializer.data['mobile']
                email = request.data['email']
                country_code = serializer.data['country_code']
                a = User.objects.create(username=request.data['mobile'])
                a.save()
                created_date = date.today()

                name=request.data['name']
                junoocategory_id=request.data['junoocategory_id']
                junoosubcategory_id=request.data['junoosubcategory_id']

                c = Customer(user_id=a.id, email=email,mobile=mobile, status=True,country_code=country_code,date=created_date,name=name,junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id,)
                c.save()
                refresh = RefreshToken.for_user(a)
                refresh['phonenumber'] = a.username
                cus = Customer.objects.get(id=c.id)
                refresh['customer'] = cus.id
                refresh['junoocategory_id'] = request.data['junoocategory_id']
                refresh['junoosubcategory_id'] = request.data['junoosubcategory_id']
                junnocatsdata = junoocategory.objects.filter(status=True)
                if junnocatsdata is not None:
                    resd = []
                    for jc in junnocatsdata:
                        subres = []
                        if jc.get_junnosubcats is not None:
                            for sjc in jc.get_junnosubcats:
                                subtemps = {
                                    "junoosubcatid": sjc.id,
                                    "junoosubcattitle": sjc.title,
                                }
                                subres.append(subtemps)

                        tempdata = {
                            "junoocatid": jc.id,
                            "title": jc.title,
                            "subcats": subres
                        }
                        resd.append(tempdata)
                else:
                    resd = None
                res = {'already_user':True,'junoocats':resd,'refresh': str(refresh), 'access': str(refresh.access_token)}
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
class question_subject_lists(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        subjectlist = subject.objects.filter(status=True,junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id)
        subjectlistdata=[]
        if subjectlist is not None:
            for sl in subjectlist:
                subject_chapters=[]
                for schp in sl.get_chapters:
                    tempchtp={
                        "chapter_id":schp.id,
                        "chapter_title": schp.title,
                    }
                    subject_chapters.append(tempchtp)
                tesub={
                    "subject_id":sl.id,
                    "subject_title":sl.title,
                    "subject_chapters":subject_chapters
                }
                subjectlistdata.append(tesub)
        return response(True, "success", subjectlistdata)

class doyouknowdata(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        doyodata = doyouknow.objects.filter(status=True,junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id)
        if doyodata is not None:
            data = []
            for dd in doyodata:

                temda={
                    "id":dd.id,
                    "title":dd.title,
                    "details":dd.details,
                    "img":dd.img.url,
                    "thumb": dd.thumb.url
                }
                data.append(temda)
        else:
            data=[]
        return response(True, "success", data)

class  HomePage(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        if customer_id :
                userdtd = Customer.objects.get(id=customer_id)
                user_info={
                    "name":userdtd.name,
                    "phoneNumber": userdtd.mobile,
                    "email": userdtd.email,
                    "country_code": userdtd.country_code,
                    "date_created": userdtd.date,
                    "image":"",
                    "level":"level",
                    "badge":"badge",
                    "achievedPoints":100,
                    "blockedUser":False,
                    "blackedReason":""
                }
                welcomedata = appopen_data.objects.all()
                sliderlist = slider.objects.filter(status=True,)
                if sliderlist is not None:
                    sliderdata=[]
                    for si in sliderlist:
                        temoslider={
                            "slider_id": si.id,
                            "image": si.img.url,
                            "screen": si.screen,
                            "args": {
                                "screen_id":si.appscreen_id,
                                "title": si.title,
                            },
                            "link": si.extra_link
                        }
                        sliderdata.append(temoslider)
                else:
                    sliderdata=[]


                if welcomedata:
                    welcometitle=welcomedata[0].title
                    welcome_note = welcomedata[0].details
                else:
                    welcometitle="Jonooo!"
                    welcome_note="Junooo "

                welcomeNote={
                    "title":welcometitle+userdtd.name,
                    "desc":welcome_note
                }

                discoverApp = {
                    "image": "https://user-images.githubusercontent.com/105601050/199044670-249db792-b3dc-4d52-97b2-2e7d3a2b5fcb.png",
                    "link": "http://junooapp.in/"
                }
                data = {
                    "welcomeNote":welcomeNote,
                    "discoverApp": discoverApp,
                    "slider":sliderdata,
                    "user":user_info,
                }
        else:
            data = None


        return response(True, "success", data)

class MainLeaderBoard(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        data=[]

        for i in range(100):
            temp = {
                "userId": "1001",
                "userName": "demo",
                "userImage": "/media/slider/ms-dhoni-1200.jpeg",
                "point": i
            }
            data.append(temp)
        return response(True, "success", data)

class SelectedExamsHomePage(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        data = []
        temp = {
            "id": "1001",
            "title": "quize",
            "desc": "test data",
            "image": "/media/doyouknow/Group_11309_copy_GfdrmMh.png",
            "sectionfinder":"",
            "selectedexam_tbl_id":123
        }
        data.append(temp)
        return response(True, "success", data)