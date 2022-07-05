from django.urls import  path
from . import views

app_name = 'judge'
urlpatterns = [
    path('', views.index , name="index"),
    path('problems/' , views.problems , name="problems"),
    path('problem/<int:problem_id>/' , views.problem , name="problem"),
    path('submit/<int:pid>/' , views.submit , name="submit"),
    path('submit/<str:status>/' , views.result , name="result"),
    path('submissions/' , views.submissions , name="submissions"),
    path("register/", views.register_request, name="register")
]