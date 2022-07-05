from sqlite3 import Timestamp
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Problem(models.Model):
    Difficulty_choices = (
    ('difficult' , 'difficult'),
    ('medium' , 'medium'),
    ('easy' , 'easy'),
    )
    problem_name = models.CharField(max_length=50)
    problem_desc = models.TextField()
    problem_difficulty = models.CharField(max_length=10, choices=Difficulty_choices)

    def __str__(self):
        return self.problem_name

class Test(models.Model):
    problem = models.ForeignKey(Problem , on_delete=models.CASCADE)
    test_input = models.FileField( upload_to='test_inputs/',null=False)
    test_output = models.FileField( upload_to='test_outputs/',null=False)



class Solution(models.Model):
    Language_choices = (
        ('c++' , 'cpp'),
    )
    Verdict_choices = (
        ('PS' , 'Processing'),
        ('WA' , 'Wrong Answer'),
        ('AC' , 'All Correct'),
        ('TLE' , 'Time Limit Exeeded'),
        ('MLE' , 'Memory Limit Exeeded'),
    )
    problem = models.ForeignKey(Problem , on_delete=models.CASCADE)
    language = models.CharField(max_length=10 , choices=Language_choices)
    code_file = models.FileField(upload_to='code_file/' , null=False)
    verdict = models.CharField(max_length=5 , choices=Verdict_choices)
    timestamp = models.TimeField(auto_now_add=True)