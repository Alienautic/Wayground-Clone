from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import random
import string

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1)

    def __str__(self):
        return self.text
    

class Attempt(models.Model):
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE
    )
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"