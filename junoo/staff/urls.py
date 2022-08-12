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


]
