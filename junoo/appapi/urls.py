from django.urls import path,include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path('JunooCats', JunooCats.as_view()),
    path('GetOtp', GetOtp.as_view()),
    path('VerifyOtp', VerifyOtp.as_view()),
    path('RegisterUser', RegisterUser.as_view()),
    path('HomePage', HomePage.as_view()),
    path('doyouknow', doyouknowdata.as_view()),
    path('MainLeaderBoard', MainLeaderBoard.as_view()),
    path('SelectedExams', SelectedExamsHomePage.as_view()),
    path('question_subject_lists', question_subject_lists.as_view()),
    path('chapterListBySubject', chapterListBySubject.as_view()),
    path('QuizeList', QuizeList.as_view()),
    path('QANDALog', QANDALog.as_view()),
    path('QAAQuations', QAAQuations.as_view()),
    path('quizeHistorySave', quizeHistorySave.as_view()),
    path('ExamHistorySave', ExamHistorySave.as_view()),

    # path('QuizeHistoryDetailsSave', QuizeHistoryDetailsSave.as_view()),
    path('QuizeQuestions', QuizeQuestions.as_view()),
    path('ExamCategoryList', ExamCategoryList.as_view()),
    path('ExamList', ExamListdata.as_view()),
    path('ExamQuestions', ExamQuestions.as_view()),
    path('QuizeLandingPage', QuizeLandingPage.as_view()),
    path('ExamLandingPage', ExamLandingPage.as_view()),


    path('TotalBalancePoint', TotalBalancePoint.as_view()),

    path('UserDetails', UserDetails.as_view()),

    path('SPExamCard', SPExamCard.as_view()),
    path('SPExamLandingPage', SPExamLandingPage.as_view()),
    path('SPExamQuestions', SPExamQuestions.as_view()),
    path('SPExamHistorySave', SPExamHistorySave.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('Historys', Historys.as_view()),
    path('HistoryList', HistoryList.as_view()),

    path('AttemptList', AttemptList.as_view()),

    path('ProfileEdit', ProfileEdit.as_view()),
    path('ProfileJunooCatEdit', ProfileJunooCatEdit.as_view()),

    path('PointHistoryListPage', PointHistoryListPage.as_view()),

]
