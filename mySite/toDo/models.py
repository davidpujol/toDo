from django.db import models
from datetime import datetime

# Create your models here.

class User (models.Model):
    user = models.CharField(max_length=25, default=None)
    password = models.CharField(max_length=50, default=None)
    name = models.CharField(max_length=100, default=None)
    age = models.IntegerField(default=18)
    email = models.CharField(max_length=100, default=None)
    confirmed = models.BooleanField(default=False)




class ToDoList(models.Model):
    title = models.CharField(max_length=50, default="MY_LIST")
    date = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class SingleTask(models.Model):
    task = models.CharField(max_length=200, default="EMPTY_TASK")
    completed = models.BooleanField(default=False)
    list = models.ForeignKey(ToDoList, on_delete = models.CASCADE)
