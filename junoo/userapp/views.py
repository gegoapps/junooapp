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

def HomePage(request):
    return render(request, 'index.html')

