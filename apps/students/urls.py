from django.urls import path
from . import views

urlpatterns = [

    # STUDENT URLS
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_logout',
         views.student_logout, name='student_logout'),
]
