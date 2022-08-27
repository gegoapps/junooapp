from django.urls import path,include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path('JunooCats', JunooCats.as_view()),
    path('GetPhoneNumber', GetPhoneNumber.as_view()),
    path('GetOtp', GetOtp.as_view()),
    path('RegisterUser', RegisterUser.as_view()),
    path('HomePage', HomePage.as_view()),
    path('doyouknow', doyouknowdata.as_view()),
    path('question_subject_lists', question_subject_lists.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
