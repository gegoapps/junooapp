from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . models import *
from masters import *
from questions import *

from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from questions.models import subject,chapter,questions

from appapi.models import Customer

from masters.models import doyouknow

from quizes.models import quize


def login(request):
    username = request.session.get('username')
    if username:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            cus = Staff.objects.filter(username=username,password=password)
            print(cus)
            if cus :
                user = authenticate(request,username=username,password=password)

                if user is not None:
                    auth_login(request, user)
                    request.session['username']=user.username
                    return redirect('dashboard')
                else:
                    messages.info(request, "Username or Password Is Incorrect")
                    return render(request, 'login.html',)

            else:
                messages.info(request,"Username or Password Is Incorrect")
                return render(request, 'login.html', {'dat': 'dat'})

        return  render(request,'login.html',{'dat':'dat'})

def dashboard(request):
    if  request.user.is_authenticated:
        return  render(request,"dashboard.html")
    else:
        return redirect("login")
def junoocategorys(request):
    res = junoocategory.objects.all()
    return  render(request,"junoocategory.html",{'res':res})

def junoocategory_create(request):
    if request.method == 'POST':
        title =request.POST.get('title')
        res =junoocategory(title=title,status=False)
        res.save()
        messages.info(request, "Success")
        return render(request,'junoocategory_create.html',)

    else:
        return render(request,'junoocategory_create.html',)


def junoocategory_edit(request,pk):
    catdata = junoocategory.objects.get(id=pk)
    if request.method == 'POST':
        catdata.title =request.POST.get('title')
        catdata.status=False
        catdata.save()
        messages.info(request, "Updated")
        return render(request,'junoocategory_create.html',{'catdata':catdata})

    else:
        return render(request,'junoocategory_create.html',{'catdata':catdata})

def junoosubcategorys(request,pk):
    res = junoosubcategory.objects.filter(junoocategory_id=pk)
    maincat = junoocategory.objects.filter(id=pk)

    return render(request, 'junoosubcategory.html', {'mainid':pk,'res':res,'maincat':maincat[0].title})






def junoosubcategory_create(request,pk):
    maincat = junoocategory.objects.filter(id=pk)

    if request.method == 'POST':
        title =request.POST.get('title')
        mainid = request.POST.get('mainid')
        res =junoosubcategory(title=title,status=False,junoocategory_id=mainid)
        res.save()
        messages.info(request, "Success")
        return render(request,'junoosubcategory_create.html',{'mainid':pk,'maincat':maincat[0].title})

    else:
        return render(request,'junoosubcategory_create.html',{'mainid':pk,'maincat':maincat[0].title})



def subjects(request,pk):
    subcatid=pk
    subcatdetails = junoosubcategory.objects.filter(id=pk)
    res = subject.objects.filter(junoosubcategory_id=pk)
    subjectdeatils={
        "title":subcatdetails[0].title,
        "subid":subcatdetails[0].id
    }
    return render(request, 'subjects.html', {'res':res,'subjectdeatils':subjectdeatils})

def subject_create(request,pk):
    subcat = junoosubcategory.objects.get(id=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        mainid = request.POST.get('mainid')
        subid = request.POST.get('subid')
        res = subject(title=title, status=False, junoocategory_id=mainid,junoosubcategory_id=subid)
        res.save()
        messages.info(request, "Success")
        return render(request, 'subject_create.html', {'subcat': subcat,})

    else:
        return render(request, 'subject_create.html', {'subcat': subcat,})

def chapters(request,pk):
    subjectid = pk
    subjectdetails = subject.objects.filter(id=subjectid)
    res = chapter.objects.filter(subject_id=pk)
    subjectdeatils = {
        "title": subjectdetails[0].title,
        "subjectid": subjectdetails[0].id,

    }
    return render(request, 'chapters.html', {'res': res, 'subjectdeatils': subjectdeatils})

def chapter_create(request,pk):

    subcat = subject.objects.get(id=pk)

    if request.method == 'POST':
        title = request.POST.get('title')

        subid = request.POST.get('subid')
        res = chapter(title=title, status=False, subject_id=subid)
        res.save()
        messages.info(request, "Success")
        return render(request, 'chapter_create.html', {'subcat': subcat,})

    else:
        return render(request, 'chapter_create.html', {'subcat': subcat,})

def questions_list(request,pk):
    chapterid=pk
    questionslist = questions.objects.filter(chapter_id=chapterid).order_by("-id")
    return render(request, 'questions.html',{'questionslist':questionslist,'chapterid':chapterid} )

def  create_questions(request,pk):

    chapterdata = chapter.objects.get(id=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answer = request.POST.get('answer')
        cf_date = request.POST.get('cf_date')
        current_affair = request.POST.get('current_affair')
        chapterid = request.POST.get('chapterid')
        chapterdata = chapter.objects.get(id=chapterid)
        junoocategory_id=chapterdata.subject.junoocategory_id
        junoosubcategory_id=chapterdata.subject.junoosubcategory_id
        cdate=datetime.datetime.now()
        res = questions(current_affairs=current_affair,current_affairs_date=cf_date,junoocategory_id=junoocategory_id, junoosubcategory_id=junoosubcategory_id, subject=chapterdata.subject,chapter_id=chapterid,created_date=cdate,status=False,verification=False,title=title,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer)
        res.save()
        messages.info(request, "Success")
        return render(request, 'create_question.html', {'chapterdata': chapterdata,})

    else:
        return render(request, 'create_question.html', {'chapterdata': chapterdata,})

def Question_Edit(request,chapterid,qid):
    chapterdata = chapter.objects.get(id=chapterid)
    questiondata = questions.objects.get(id=qid)
    if request.method == 'POST':
        questiondata.title = request.POST.get('title')
        questiondata.option1 = request.POST.get('option1')
        questiondata.option2 = request.POST.get('option2')
        questiondata.option3 = request.POST.get('option3')
        questiondata.option4 = request.POST.get('option4')
        questiondata.answer = request.POST.get('answer')
        questiondata.current_affairs_date = request.POST.get('cf_date')
        questiondata.current_affairs = request.POST.get('current_affair')
        questiondata.chapter_id = request.POST.get('chapterid')
        chapterdata = chapter.objects.get(id=chapterid)
        questiondata.subject=chapterdata.subject

        questiondata.verification=False
        questiondata.status=False
        questiondata.junoocategory_id=chapterdata.subject.junoocategory_id
        questiondata.junoosubcategory_id=chapterdata.subject.junoosubcategory_id
        questiondata.created_date=datetime.datetime.now()

        questiondata.save()
        messages.info(request, "Updated")
        return render(request, 'create_question.html', {'chapterdata': chapterdata,'questiondata':questiondata})

    else:
        return render(request, 'create_question.html', {'chapterdata': chapterdata,'questiondata':questiondata})

def UserList(request):
    res = Customer.objects.all()
    return  render(request,"UserList.html",{'res':res})

def doyouKnowList(request):
    res = doyouknow.objects.all()
    return  render(request,"doyouKnow.html",{'res':res})

def logout_view(request):
    logout(request)
    return  redirect("login")

def quizList(request):
    res = quize.objects.all()

    return  render(request,'quize_list.html',{'res':res})

def mocktests(request):
    return  HttpResponse("Coming Soon")

def exams(request):
    return  HttpResponse("Coming Soon")

def practices(request):
    return  HttpResponse("Coming Soon")

def quiz_questions_list(request,pk):

    return  HttpResponse("dd")

def create_quiz(request):
    return  HttpResponse("Coming Soon")