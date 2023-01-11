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
                created_date = date.today()
                title = "Welcome Sweets"
                p = PointHistory(customer_id=c.id, created_date=created_date, created_point=1000,title=title, status=True, used_or_get=False)
                p.save()
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
                    "chapter_count":len(sl.get_chapters),
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
                    "image":"/media/customers/nouser.png",
                    "level":"level",
                    "badge":"badge",
                     "achievedPoints": userdtd.current_totalpoint,
            "blockedUser": userdtd.isBlocked,
            "blockedReason": userdtd.blockedReason,
                    "junoocategory_id": userdtd.junoocategory.id,
                    "junoocategory_title": userdtd.junoocategory.title,
                    "junooSubcategory_id": userdtd.junoosubcategory.id,
                    "junooSubcategory_title": userdtd.junoosubcategory.title,
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
                    welcometitle=welcomedata[0].title+" "
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

        # for i in range(100):
        #     temp = {
        #         "userId": "1001",
        #         "userName": "demo",
        #         "userImage": "/media/slider/ms-dhoni-1200.jpeg",
        #         "point": i
        #     }
        #     data.append(temp)
        return response(True, "success", data)

class SelectedExamsHomePage(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        data = []
        # temp = {
        #     "id": "1001",
        #     "title": "quize",
        #     "desc": "test data",
        #     "image": "/media/doyouknow/Group_11309_copy_GfdrmMh.png",
        #     "sectionfinder":"",
        #     "selectedexam_tbl_id":123
        # }
        # data.append(temp)
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
            quizelistdata = quize.objects.get(id=quizeid)
            cus = Customer.objects.get(id=customer_id)
            if (cus.current_totalpoint == None):
                ctpoint = 0
                examcutpoint = 0
            else:
                ctpoint = cus.current_totalpoint
                examcutpoint = quizelistdata.entry_fee

            totalpoin = int(ctpoint) - int(examcutpoint)
            cus.current_totalpoint = totalpoin
            cus.save()
            created_date = date.today()
            title = "Quize  Attented"
            c = PointHistory(customer_id=customer_id, created_date=created_date, created_point=examcutpoint,title=title, status=True, used_or_get=True)
            c.save()

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
        is_passed = request.data['is_passed']
        earnedpoint = request.data['earnedpoint']
        created_date = date.today()
        a=QuizeHistory(created_time=datetime.datetime.now().time(),created_date=date.today(),is_passed=is_passed,earnedpoint=earnedpoint,quize_id=quizeid,customer_id=customer_id,quize_attended_code=randomid,total_questions=total_questions,total_right_answers=total_right_answers,total_wrong_answer=total_wrong_answer)
        a.save()
        questiondata = request.data['questiondata']
        for k in questiondata:
            b=Quize_attended_questions(quize_id=quizeid,customer_id=customer_id,quize_attended_code=randomid,quizehistory_id=a.id,question_id=k['question'],right_wrong=k['right_wrong'],crt_option=k['crt_option'],selected_ans=k['selected_ans'])
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
            c=PointHistory(customer_id=customer_id,created_date=created_date,created_point=earnedpoint,title=title,status=True,used_or_get=False)
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
            cus = Customer.objects.get(id=customer_id)

            if (cus.current_totalpoint == None):
                ctpoint = 0
            else:
                ctpoint = cus.current_totalpoint
            temp={
                "quize_db_id": quizelist.id,
                "quize_code": quizelist.quize_id,
                "title": quizelist.title,
                "win_price": quizelist.win_price,
                "entry_fee": quizelist.entry_fee,
                "tot_time": quizelist.quize_time,
                "total_point":00,
                "total_questions": 00,
                "quize_tag": quizelist.quize_tag,
                "quize_emoji": quizelist.quize_emojy,
                "quize_primary_color": quizelist.quize_primary_color,
                "quize_secondary_color": quizelist.quize_secondary_color,
                "quize_details": quizelist.quize_details,

                "quize_cutoffmark": int(quizelist.quize_cutoffmark),


            }

            res={
                "quizDetails":temp,
                "leaderboard": leaderboard,
                "total_points":int(ctpoint)

            }



        else:
            res=[]
        return response(True, "success", res)


class ExamListdata(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        examcategory = request.data['examcategory']
        pre_or_moc = request.data['pre_or_moc']

        exmlist = ExamList.objects.filter(pre_or_moc=pre_or_moc,ExamCategorys_id=examcategory,junoocategory_id=junoocategory_id, junoosubcategory_id=junoosubcategory_id,status=True)
        if exmlist is not None:
            exmlistarr = []
            for i in exmlist:
                temp = {
                    "el_db_id": i.id,
                    "el_code": i.el_id,
                    "title": i.title,
                    "win_price": i.win_price,
                    "entry_fee": i.entry_fee,
                    "no_of_questions": 100,
                    "el_tag": i.el_tag,
                    "el_emoji": i.el_emojy,
                    "el_primary_color": i.el_primary_color,
                    "el_secondary_color": i.el_secondary_color,
                    "el_details": i.el_details,

                }
                exmlistarr.append(temp)
        else:
            exmlistarr = []
        return response(True, "success", exmlistarr)


class ExamLandingPage(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        examid = request.data['examid']
        exmlistdata = ExamList.objects.get(id=examid,status=True)
        if exmlistdata is not None:
            leaderboard=[]
            for i in range(1, 11):
                qq={
                    "userId": "100"+str(i),
                    "userName": "demo",
                    "userImage": "/media/slider/ms-dhoni-1200.jpeg",
                    "point": i
                }
                leaderboard.append(qq)
            cus = Customer.objects.get(id=customer_id)

            if (cus.current_totalpoint == None):
                ctpoint = 0
            else:
                ctpoint = cus.current_totalpoint
            temp={
                "el_db_id": exmlistdata.id,
                "el_code": exmlistdata.el_id,
                "title": exmlistdata.title,
                "win_price": exmlistdata.win_price,
                "entry_fee": exmlistdata.entry_fee,
                "tot_time": exmlistdata.el_time,
                "total_point":00,
                "total_questions": 00,
                "el_tag": exmlistdata.el_tag,
                "el_emoji": exmlistdata.el_emojy,
                "el_primary_color": exmlistdata.el_primary_color,
                "el_secondary_color": exmlistdata.el_secondary_color,
                "el_details": exmlistdata.el_details,

                "el_cutoffmark": exmlistdata.el_cutoffmark,
                "el_positivemark": exmlistdata.el_positivemark,
                "negativemark": exmlistdata.negativemark,


            }


            res={
                "examDetails":temp,
                "leaderboard": leaderboard,
                "total_points":int(ctpoint)

            }



        else:
            res=[]
        return response(True, "success", res)





class ExamQuestions(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']

        examid = request.data['examid']

        exmquestions = exam_questions.objects.filter(ExamList_id=examid)
        if exmquestions :
            exmlistdata = ExamList.objects.get(id=examid)
            cus = Customer.objects.get(id=customer_id)
            if (cus.current_totalpoint == None):
                ctpoint = 0
                examcutpoint=0
            else:
                ctpoint = cus.current_totalpoint
                examcutpoint = exmlistdata.entry_fee

            totalpoin = int(ctpoint) - int(examcutpoint)
            cus.current_totalpoint = totalpoin
            cus.save()
            created_date = date.today()
            title = "Exam Atempted "
            c = PointHistory(customer_id=customer_id, created_date=created_date, created_point=examcutpoint, title=title,status=True, used_or_get=True)
            c.save()
            exmquestionsarr=[]
            for qq in exmquestions:
                options = [qq.questions.option1, qq.questions.option2, qq.questions.option3, qq.questions.option4]
                temp = {
                    "question_id": qq.questions.id,
                    "question": qq.questions.title,
                    "options": options,
                    "answer": int(qq.questions.answer),

                }
                exmquestionsarr.append(temp)

            return response(True, "success", exmquestionsarr)
        else:
            return response(True, "Quize Questions are not updated . Try after some time", None)


class ExamHistorySave(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        examid = request.data['examid']
        randomid = random.randrange(10000, 10000000000)
        total_questions=request.data['total_questions']
        total_right_answers = request.data['total_right_answers']
        total_wrong_answer = request.data['total_wrong_answer']
        totalmark = request.data['totalmark']
        is_passed = request.data['is_passed']
        earnedpoint = request.data['earnedpoint']

        a=ExamHistory(created_time=datetime.datetime.now().time(),created_date = date.today(),is_passed=is_passed,earnedpoint=earnedpoint,ExamList_id=examid,customer_id=customer_id,exam_attended_code=randomid,total_questions=total_questions,total_right_answers=total_right_answers,total_wrong_answer=total_wrong_answer,total_mark=totalmark)
        a.save()
        questiondata = request.data['questiondata']
        for k in questiondata:
            b=Exam_attended_questions(ExamList_id=examid,customer_id=customer_id,exam_attended_code=randomid,ExamHistory_id=a.id,question_id=k['question'],right_wrong=k['right_wrong'],crt_option=k['crt_option'],selected_ans=k['selected_ans'])
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
            title="exam win prize"
            c=PointHistory(customer_id=customer_id,created_date=created_date,created_point=earnedpoint,title=title,status=True,used_or_get=False)
            c.save()
        resd={
            "history_id":a.id,
            "history_code":randomid
        }
        return response(True, "Success", resd)



class SPExamCard(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']

        exmlistdata = specialExam.objects.filter(status=True)

        if exmlistdata is not None:

            temp={
                "el_db_id": exmlistdata[0].id,
                "el_code": exmlistdata[0].el_id,
                "title": exmlistdata[0].title,
                "win_price": exmlistdata[0].win_price,
                "entry_fee": exmlistdata[0].entry_fee,
                "tot_time": exmlistdata[0].el_time,
                "total_point":1234,
                "deatils": exmlistdata[0].el_details,
                "el_tag": exmlistdata[0].el_tag,
                "el_emoji": exmlistdata[0].el_emojy,
                "el_primary_color": exmlistdata[0].el_primary_color,
                "el_secondary_color": exmlistdata[0].el_secondary_color,


                "el_cutoffmark": exmlistdata[0].el_cutoffmark,
                "el_positivemark": exmlistdata[0].el_positivemark,
                "negativemark": exmlistdata[0].negativemark,

                "result_published": exmlistdata[0].result_published,
                "published": exmlistdata[0].published,
                "howmany_winners": exmlistdata[0].opportunity_to_get_mark,
                "publishtime": exmlistdata[0].publishtime,

            }
            res=[]
            res={
                "examDetails":temp,

                "total_points":12432

            }
        else:
            res=None

        return response(True, "success", res)

class TotalBalancePoint(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        cus = Customer.objects.get(id=customer_id)

        if (cus.current_totalpoint == None):
            ctpoint = 0
        else:
            ctpoint = cus.current_totalpoint
        return response(True, "success", ctpoint)


class UserDetails(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']

        userdtd = Customer.objects.get(id=customer_id)
        user_info = {
            "name": userdtd.name,
            "phoneNumber": userdtd.mobile,
            "email": userdtd.email,
            "country_code": userdtd.country_code,
            "date_created": userdtd.date,
            "image": "/media/customers/nouser.png",
            "level": "level",
            "badge": "badge",
            "achievedPoints": userdtd.current_totalpoint,
            "blockedUser": userdtd.isBlocked,
            "blockedReason": userdtd.blockedReason,
            "junoocategory_id": userdtd.junoocategory.id,
            "junoocategory_title": userdtd.junoocategory.title,
            "junooSubcategory_id": userdtd.junoosubcategory.id,
            "junooSubcategory_title": userdtd.junoosubcategory.title,
        }

        return response(True, "success", user_info)



class SPExamLandingPage(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        examid = request.data['examid']
        exmlistdata =  specialExam.objects.get(id=examid)
        if exmlistdata is not None:

            temp={
                "ex_db_id": exmlistdata.id,
                "ex_code": exmlistdata.el_id,
                "title": exmlistdata.title,
                "win_price": exmlistdata.win_price,
                "entry_fee": exmlistdata.entry_fee,
                "tot_time": exmlistdata.el_time,
                "total_point":1234,
                "total_questions": 1002,
                "el_tag": exmlistdata.el_tag,
                "el_emoji": exmlistdata.el_emojy,
                "el_primary_color": exmlistdata.el_primary_color,
                "el_secondary_color": exmlistdata.el_secondary_color,
                "el_details": exmlistdata.el_details,

                "el_cutoffmark": exmlistdata.el_cutoffmark,
                "el_positivemark": exmlistdata.el_positivemark,
                "negativemark": exmlistdata.negativemark,

                "result_published": exmlistdata.result_published,
                "published": exmlistdata.published,
                "howmany_winners": exmlistdata.opportunity_to_get_mark,
                "publishtime": exmlistdata.publishtime,



            }




        else:
            temp=None
        return response(True, "success", temp)



class SPExamQuestions(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']

        examid = request.data['examid']
        exmquestions = spexam_questions.objects.filter(specialExam_id=examid)
        if exmquestions :
            exmquestionsarr=[]
            for qq in exmquestions:
                options = [qq.questions.option1, qq.questions.option2, qq.questions.option3, qq.questions.option4]
                temp = {
                    "question_id": qq.questions.id,
                    "question": qq.questions.title,
                    "options": options,
                    "answer": int(qq.questions.answer),

                }
                exmquestionsarr.append(temp)

            return response(True, "success", exmquestionsarr)
        else:
            return response(True, "Quize Questions are not updated . Try after some time", None)





class SPExamHistorySave(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        examid = request.data['examid']
        randomid = random.randrange(10000, 10000000000)
        total_questions=request.data['total_questions']
        total_right_answers = request.data['total_right_answers']
        total_wrong_answer = request.data['total_wrong_answer']
        totalmark = request.data['totalmark']

        attended_time=created_date=date.today()
        iscutoffpassed=request.data['is_passed']
        a=SPExamHistory(created_time=datetime.datetime.now().time(),created_date = date.today(),specialExam_id=examid,customer_id=customer_id,exam_attended_code=randomid,total_questions=total_questions,total_right_answers=total_right_answers,total_wrong_answer=total_wrong_answer,total_mark=totalmark,attended_time=attended_time,iscutoffpassed=iscutoffpassed,point_claimed=False)
        a.save()
        questiondata = request.data['questiondata']
        for k in questiondata:
            b=SPExam_attended_questions(specialExam_id=examid,customer_id=customer_id,exam_attended_code=randomid,SPExamHistory_id=a.id,question_id=k['question'],right_wrong=k['right_wrong'],crt_option=k['crt_option'],selected_ans=k['selected_ans'])
            b.save()

        resd={
            "history_id":a.id,
            "history_code":randomid
        }
        return response(True, "Success", resd)




class Historys(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        type = request.data['type']
        historyid = request.data['historyid']
        code = request.data['code']
        temp=None

        if(type=='quize'):
            historymain = QuizeHistory.objects.get(quize_attended_code=code,id=historyid)
            QuestionDetails = []
            if historymain is not None:
                subtemp=[]
                for i in historymain.get_Quize_attended_questions:
                    options = [i.question.option1, i.question.option2, i.question.option3, i.question.option4]
                    subtemp = {
                        "question_id": i.question.id,
                        "question": i.question.title,
                        "options": options,
                        "answer": int(i.question.answer),
                        "sub_db_id": i.id,
                        "selected_ans": i.selected_ans,
                        "right_or_wrong": i.right_wrong,


                    }

                    QuestionDetails.append(subtemp)
                    ispassed=historymain.is_passed
                    if ispassed=="False":
                        ispassed=False
                    elif ispassed=="True":
                        ispassed=True

                    temp={
                        "history_code":historymain.quize_attended_code,
                        "total_questions": historymain.total_questions,
                        "total_right_answers": historymain.total_right_answers,
                        "total_wrong_answer": historymain.total_wrong_answer,
                        "is_passed": ispassed,
                        "earnedpoint": historymain.earnedpoint,
                        "quize_cutoff": historymain.quize.quize_cutoffmark,
                        "totalEarnedMark": historymain.total_right_answers,
                        "mark":str(len(QuestionDetails)),
                         "QuestionDetails":QuestionDetails
                    }

            else:
                temp=None
        elif(type =='exam'):
            historymain = ExamHistory.objects.get(exam_attended_code=code, id=historyid)

            QuestionDetails = []
            if historymain is not None:
                subtemp=[]
                for i in historymain.get_Exam_attended_questions:
                    options = [i.question.option1, i.question.option2, i.question.option3, i.question.option4]
                    subtemp = {
                        "question_id": i.question.id,
                        "question": i.question.title,
                        "options": options,
                        "answer": int(i.question.answer),
                        "sub_db_id": i.id,
                        "selected_ans": i.selected_ans,
                        "right_or_wrong": i.right_wrong,

                    }
                    QuestionDetails.append(subtemp)
                    ispassed = historymain.is_passed
                    if ispassed == "False":
                        ispassed = False
                    elif ispassed == "True":
                        ispassed = True
                    temp = {
                        "history_code": historymain.exam_attended_code,
                        "total_questions": historymain.total_questions,
                        "total_right_answers": historymain.total_right_answers,
                        "total_wrong_answer": historymain.total_wrong_answer,
                        "is_passed": ispassed,
                        "earnedpoint": historymain.earnedpoint,
                        "quize_cutoff": historymain.ExamList.el_cutoffmark,
                        "totalEarnedMark": historymain.total_mark,
                        "mark":str(int(historymain.ExamList.el_positivemark)*len(QuestionDetails)),

                        "QuestionDetails": QuestionDetails
                    }

            else:
                temp = None
        elif (type == 'spexam'):
            historymain = SPExamHistory.objects.get(exam_attended_code=code, id=historyid)

            QuestionDetails = []
            if historymain is not None:
                subtemp=[]
                for i in historymain.get_SPExam_attended_questions:
                    options = [i.question.option1, i.question.option2, i.question.option3, i.question.option4]
                    subtemp = {
                        "question_id": i.question.id,
                        "question": i.question.title,
                        "options": options,
                        "answer": int(i.question.answer),
                        "sub_db_id": i.id,
                        "selected_ans": i.selected_ans,
                        "right_or_wrong": i.right_wrong,
                    }
                    QuestionDetails.append(subtemp)
                    ispassed = historymain.is_passed
                    if ispassed == "False":
                        ispassed = False
                    elif ispassed == "True":
                        ispassed = True
                    temp = {
                        "history_code": historymain.exam_attended_code,
                        "total_questions": historymain.total_questions,
                        "total_right_answers": historymain.total_right_answers,
                        "total_wrong_answer": historymain.total_wrong_answer,
                         "is_passed": ispassed,
                        "earnedpoint": historymain.earnedpoint,
                        "quize_cutoff": historymain.specialExam.el_cutoffmark,
                        "totalEarnedMark": historymain.total_mark,
                        "mark": str(int(historymain.specialExam.el_positivemark) * len(QuestionDetails)),
                        "QuestionDetails": QuestionDetails
                    }

            else:
                temp = None

        return response(True, "Success", temp)



class HistoryList(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        type = request.data['type']
        resd=[]


        if (type == 'quize'):
            quizelistattended = QuizeHistory.objects.filter(customer_id=customer_id).values('quize').distinct()

            if quizelistattended is not None:
                for qa in quizelistattended:

                    quizedata = quize.objects.get(id=qa['quize'])

                    lastattendeddate = QuizeHistory.objects.filter(customer_id=customer_id,quize_id=quizedata.id).order_by('-created_date')
                    temp = {
                        "historyListId": quizedata.id,
                        "historyListTitle": quizedata.title,
                        "historyListType":type,
                        "historyListLastAtemptDate":lastattendeddate[0].created_date.strftime("%d-%b-%y"),
                        "created_time": lastattendeddate[0].created_time.strftime("%I:%M %p"),

                    }
                    resd.append(temp)

            else:
                resd = []
        elif (type == 'exam'):
            quizelistattended = ExamHistory.objects.filter(customer_id=customer_id).values('ExamList').distinct()
            if quizelistattended is not None:
                for qa in quizelistattended:

                    quizedata = ExamList.objects.get(id=qa['ExamList'])
                    lastattendeddate = ExamHistory.objects.filter(customer_id=customer_id,ExamList_id=quizedata.id).order_by('-created_date')


                    temp = {
                        "historyListId": quizedata.id,
                        "historyListTitle": quizedata.title,
                        "historyListType": type,
                        "historyListLastAtemptDate": lastattendeddate[0].created_date.strftime("%d-%b-%y"),
                        "created_time": lastattendeddate[0].created_time.strftime("%I:%M %p"),

                    }
                    resd.append(temp)

            else:
                resd = []
        elif (type == 'spexam'):
            quizelistattended = SPExamHistory.objects.filter(customer_id=customer_id).values('specialExam').distinct()
            if quizelistattended is not None:
                for qa in quizelistattended:
                    quize_historys = []
                    quizedata = specialExam.objects.get(id=qa['specialExam'])
                    lastattendeddate = ExamHistory.objects.filter(customer_id=customer_id,specialExam_id=quizedata.id).order_by('-created_date')


                    temp = {
                        "historyListId": quizedata.id,
                        "historyListTitle": quizedata.title,
                        "historyListType": type,
                        "historyListLastAtemptDate": lastattendeddate[0].created_date.strftime("%d-%b-%y"),
                        "created_time": lastattendeddate[0].created_time.strftime("%I:%M %p"),

                    }
                    resd.append(temp)

            else:
                resd = []


        return response(True, "Success", resd)


class AttemptList(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        id = request.data['id']
        type = request.data['type']
        res=[]
        if (type == 'quize'):
            historylist = QuizeHistory.objects.filter(customer_id=customer_id, quize_id=id).order_by('-id')
            for hl in historylist:
                lltmp = {
                    "history_id": hl.id,
                    "history_code": hl.quize_attended_code,
                    "type":type,
                    "created_date":hl.created_date.strftime("%d-%b-%y"),
                     "created_time": hl.created_time.strftime("%I:%M %p"),
                }
                res.append(lltmp)
        elif(type == 'spexam'):
            historylist = SPExamHistory.objects.filter(customer_id=customer_id, specialExam_id=id).order_by('-id')

            for hl in historylist:
                lltmp = {
                    "history_id": hl.id,
                    "history_code": hl.exam_attended_code,
                    "created_date": hl.created_date.strftime("%d-%b-%y"),
                     "created_time": hl.created_time.strftime("%I:%M %p"),


                }
                res.append(lltmp)
        elif (type == 'exam'):
            historylist = ExamHistory.objects.filter(customer_id=customer_id, ExamList_id=id).order_by('-id')

            for hl in historylist:
                lltmp = {
                    "history_id": hl.id,
                    "history_code": hl.exam_attended_code,
                    "created_date": hl.created_date.strftime("%d-%b-%y"),
                    "created_time": hl.created_time.strftime("%I:%M %p"),
                }
                res.append(lltmp)




        return response(True, "Success", res)




class ProfileEdit(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        name = request.data['name']
        email = request.data['email']
        userdtd = Customer.objects.get(id=customer_id)
        userdtd.name=name
        userdtd.email=email
        userdtd.save()
        userdtd = Customer.objects.get(id=customer_id)
        user_info = {
            "name": userdtd.name,
            "phoneNumber": userdtd.mobile,
            "email": userdtd.email,
            "country_code": userdtd.country_code,
            "date_created": userdtd.date,
            "image": "/media/customers/nouser.png",
            "level": "level",
            "badge": "badge",
            "achievedPoints": userdtd.current_totalpoint,
            "blockedUser": userdtd.isBlocked,
            "blockedReason": userdtd.blockedReason,
            "junoocategory_id": userdtd.junoocategory.id,
            "junoocategory_title": userdtd.junoocategory.title,
            "junooSubcategory_id": userdtd.junoosubcategory.id,
            "junooSubcategory_title": userdtd.junoosubcategory.title,
        }

        return response(True, "Success", user_info)


class ProfileJunooCatEdit(APIView):
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']
        newjunooid = request.data['junoid']
        newjunoosubid = request.data['junosubid']

        userdtd = Customer.objects.get(id=customer_id)


        userdtd.junoocategory_id=int(newjunooid)
        userdtd.junoosubcategory_id=int(newjunoosubid)
        userdtd.save()
        userdtds = Customer.objects.get(id=customer_id)
        a = User.objects.get(username=userdtds.mobile)

        refresh = RefreshToken.for_user(a)
        refresh['phonenumber'] = a.username

        refresh['customer'] = userdtds.id
        refresh['junoocategory_id'] = userdtds.junoocategory_id
        refresh['junoosubcategory_id'] = userdtds.junoosubcategory_id

        user_info = {
            "name": userdtds.name,
            "phoneNumber": userdtds.mobile,
            "email": userdtds.email,
            "country_code": userdtds.country_code,
            "date_created": userdtds.date,
            "image": "",
            "level": "level",
            "badge": "badge",
            "achievedPoints": userdtds.current_totalpoint,
            "blockedUser": userdtds.isBlocked,
            "blockedReason": userdtds.blockedReason,
            "junoocategory_id": userdtds.junoocategory.id,
            "junoocategory_title": userdtds.junoocategory.title,
            "junooSubcategory_id": userdtds.junoosubcategory.id,
            "junooSubcategory_title": userdtds.junoosubcategory.title,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }





        return response(True, "Success", user_info)




class PointHistoryListPage(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        decoded = jwt.decode(token, options={"verify_signature": False})  # works in PyJWT >= v2.0
        customer_id = decoded['customer']
        junoocategory_id = decoded['junoocategory_id']
        junoosubcategory_id = decoded['junoosubcategory_id']

        listdataph = PointHistory.objects.filter(customer_id=customer_id).order_by('-id')
        userdtd = Customer.objects.get(id=customer_id)
        if listdataph is not None:
            listofhistory=[]
            totpointusedtillnow=0
            totpointugettillnow=0
            for i in listdataph:
                if(i.used_or_get==True):
                    totpointusedtillnow = int(totpointusedtillnow)+ int(i.created_point)
                else:
                    totpointugettillnow=int(totpointugettillnow)+int(i.created_point)
                qq={
                    "id": i.id,
                    "created_date": i.created_date,
                    "created_point": i.created_point,
                    "point": i.title,
                    "used_or_get":i.used_or_get
                }
                listofhistory.append(qq)
            res={

                "total_current_point":userdtd.current_totalpoint,
                "GrandTotalEarned":totpointugettillnow,
                "GrandTotalUsed":totpointusedtillnow,
                "History":listofhistory
            }

        else:
            res=None
        return response(True, "success", res)