from django.urls import path,include

from . import views

urlpatterns = [
    path('login', views.login,name="login"),
    path('', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('junoocategorys', views.junoocategorys, name="junoocategorys"),
    path('junoocategory_create', views.junoocategory_create, name="junoocategory_create"),
    path('junoosubcategorys/<str:pk>', views.junoosubcategorys, name="junoosubcategorys"),
    path('junoosubcategory_create/<str:pk>', views.junoosubcategory_create, name="junoosubcategory_create"),
    path('subjects/<str:pk>', views.subjects, name="subjects"),
    path('subject_create/<str:pk>', views.subject_create, name="subject_create"),
    path('chapters/<str:pk>', views.chapters, name="chapters"),
    path('chapter_create/<str:pk>',views.chapter_create, name="chapter_create"),
    path('questions_list/<str:pk>', views.questions_list, name="questions_list"),
    path('create_questions/<str:pk>', views.create_questions, name="create_questions"),
    path('junoocategory_edit/<str:pk>', views.junoocategory_edit, name="junoocategory_edit"),
    path('Question_Edit/<str:chapterid>/<str:qid>', views.Question_Edit, name="Question_Edit"),
    path('UserList', views.UserList, name="UserList"),
    path('doyouKnowList', views.doyouKnowList, name="doyouKnowList"),
    path('logout_view', views.logout_view, name="logout_view"),
    path('quizList', views.quizList, name="quizList"),
    path('mocktests', views.mocktests, name="mocktests"),
    path('exams', views.exams, name="exams"),
    path('practices', views.practices, name="practices"),
    path('quiz_questions_list/<str:pk>', views.quiz_questions_list, name="quiz_questions_list"),
    path('create_quiz', views.create_quiz, name="create_quiz"),
    path('create_doyouknow', views.create_doyouknow, name="create_doyouknow"),


]
