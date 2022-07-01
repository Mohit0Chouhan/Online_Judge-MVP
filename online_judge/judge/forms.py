from distutils.command.upload import upload
from django import forms

from judge.models import Solution

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class Submission_form(forms.Form):
    Language_choices = [
        ('c++' , 'cpp'),
    ]
    language = forms.Select(choices=Language_choices)
    c_file = forms.FileField()


# class SubmitSolution(forms.Form):
#     Language_choices = (
#         ('c++' , 'cpp'),
#     )
#     Verdict_choices = (
#         ('WA' , 'Wrong Answer'),
#         ('AC' , 'All Correct'),
#         ('TLE' , 'Time Limit Exeeded'),
#         ('MLE' , 'Memory Limit Exeeded'),
#     )
#     language = forms.CharField(choices=Language_choices)
#     code_file = forms.FileField()
#     verdict = forms.CharField(choices=Verdict_choices)