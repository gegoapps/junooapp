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


from questions.models import *

from quizes.models import *



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
class chapterListBySubject(APIView):
    def post(self,request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0


        subjectid = request.data['subjectid']

        chapterlist = chapter.objects.filter(status=True,subject_id=subjectid)

        if chapterlist is not None:
            chapterlistarr = []
            for ch in chapterlist:
                tempchtp = {
                    "chapter_id": ch.id,
                    "chapter_title": ch.title,
                }
                chapterlistarr.append(tempchtp)
        else:
           chapterlistarr=[]
        return response(True, "success", chapterlistarr)
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
                    "chapter_count":100,
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
class QAAQuations(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        subjectid = request.data['subjectid']
        chapterid = request.data['chapterid']
        questionlist = questions.objects.filter(junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id,subject_id =subjectid,chapter_id=chapterid,status=True,verification=True)

        if questionlist is not None:
            questionlistarr=[]
            for i in questionlist:
                options=[i.option1,i.option2,i.option3,i.option4]
                temp={
                    "question_id":i.id,
                    "question":i.title,
                    "options":options,
                    "answer": int(i.answer),

                }
                questionlistarr.append(temp)
        else:
            questionlistarr=[]

        return response(True, "success", questionlistarr)

class QANDALog(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        rightanswer = request.data['rightanswer']
        wronganswer = request.data['wronganswer']
        skippedanswers = request.data['skippedanswers']
        created_date = date.today()
        a = qanda_attended_log(customer_id=customer_id,created_date=created_date,right_answr=rightanswer,wrong_answr=wronganswer,skiped_answr=skippedanswers)
        a.save()
        return response(True, "success", None)
class QuizeList(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        quizelist = quize.objects.filter(junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id, status=True)
        if quizelist is not None:
            quizelistarr=[]
            for i in quizelist:

                temp={
                    "quize_db_id":i.id,
                    "quize_code":i.quize_id,
                    "title":i.title,
                    "win_price": i.win_price,
                    "entry_fee": i.entry_fee,
                    "no_of_questions":100,
                    "quize_tag": i.quize_tag,
                    "quize_emoji": i.quize_emojy,
                    "quize_primary_color": i.quize_primary_color,
                    "quize_secondary_color": i.quize_secondary_color,
                    "quize_details": i.quize_details,




                }
                quizelistarr.append(temp)
        else:
            quizelistarr=[]
        return response(True, "success", quizelistarr)

class QuizeQuestions(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']

        quizeid = request.data['quizeid']
        quizequestions = quize_questions.objects.filter(quize_id=quizeid)
        if quizequestions :
            questionlistarr=[]
            for qq in quizequestions:
                options = [qq.questions.option1, qq.questions.option2, qq.questions.option3, qq.questions.option4]
                temp = {
                    "question_id": qq.questions.id,
                    "question": qq.questions.title,
                    "options": options,
                    "answer": int(qq.questions.answer),

                }
                questionlistarr.append(temp)

            return response(True, "success", questionlistarr)
        else:
            return response(True, "Quize Questions are not updated . Try after some time", None)

class quizeHistorySave(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        quizeid = request.data['quizeid']
        randomid = random.randrange(10000, 10000000000)
        total_questions=request.data['total_questions']
        total_right_answers = request.data['total_right_answers']
        total_wrong_answer = request.data['total_wrong_answer']
        a=QuizeHistory(quize_id=quizeid,customer_id=customer_id,quize_attended_code=randomid,total_questions=total_questions,total_right_answers=total_right_answers,total_wrong_answer=total_wrong_answer)
        a.save()
        questiondata = request.data['questiondata']
        for k in questiondata:
            b=Quize_attended_questions(quize_id=quizeid,customer_id=customer_id,quize_attended_code=randomid,quizehistory_id=a.id,question_id=k['question'],right_wrong=k['right_wrong'],crt_option=k['crt_option'])
            b.save()
        is_passed = request.data['is_passed']
        earnedpoint = request.data['earnedpoint']
        if(is_passed==True):
            cus = Customer.objects.get(id=customer_id)
            if(cus.current_totalpoint == None):
                ctpoint=0
            else:
                ctpoint = cus.current_totalpoint
            totalpoin=int(ctpoint)+int(earnedpoint)
            cus.current_totalpoint=totalpoin
            cus.save()
            created_date=date.today()
            title="quize win prize"
            c=PointHistory(customer_id=customer_id,created_date=created_date,created_point=earnedpoint,title=title,status=True)
            c.save()
        resd={
            "history_id":a.id,
            "history_code":randomid
        }
        return response(True, "Success", resd)

# class QuizeHistoryDetailsSave(APIView):
#     def post(self, request):
#         token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
#
#         decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
#         customer_id = decoded['customer']
#         junoocategory_id = decoded['junoocategory_id']
#         junoosubcategory_id = decoded['junoosubcategory_id']
#         quizeid = request.data['quizeid']
#         Historyid = request.data['historyid']
#         historycode = request.data['historycode']
#         questiondata= request.data['questiondata']
#         for k in questiondata:
#             a=Quize_attended_questions(quize_id=quizeid,customer_id=customer_id,quize_attended_code=historycode,quizehistory_id=Historyid,question_id=k['question'],right_wrong=k['right_wrong'],crt_option=k['crt_option'])
#             a.save()
#         return response(True, "success" , None)
class ExamCategoryList(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        examcatlist = ExamsCategorys.objects.filter(junoocategory_id=junoocategory_id,junoosubcategory_id=junoosubcategory_id, status=True)
        res=[]
        if examcatlist is not None:
            for i in examcatlist:
                temp={
                    "exam_categoryId":i.id,
                    "exam_title": i.title,
                    "exam_details": i.details,
                }
                res.append(temp)
        return response(True, "success", res)
class QuizeLandingPage(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        quizeid = request.data['quizeid']
        quizelist = quize.objects.get(id=quizeid,status=True)
        if quizelist is not None:
            leaderboard=[]
            for i in range(1, 11):
                qq={
                    "userId": "100"+str(i),
                    "userName": "demo",
                    "userImage": "/media/slider/ms-dhoni-1200.jpeg",
                    "point": i
                }
                leaderboard.append(qq)
            temp={
                "quize_db_id": quizelist.id,
                "quize_code": quizelist.quize_id,
                "title": quizelist.title,
                "win_price": quizelist.win_price,
                "entry_fee": quizelist.entry_fee,
                "tot_time": quizelist.quize_time,
                "total_point":1234,
                "total_questions": 1002,
                "quize_tag": quizelist.quize_tag,
                "quize_emoji": quizelist.quize_emojy,
                "quize_primary_color": quizelist.quize_primary_color,
                "quize_secondary_color": quizelist.quize_secondary_color,
                "quize_details": quizelist.quize_details,

                "quize_cutoffmark": quizelist.quize_cutoffmark,


            }
            res=[]
            res={
                "quizDetails":temp,
                "leaderboard": leaderboard,
                "total_points":12432

            }



        else:
            res=[]
        return response(True, "success", res)



