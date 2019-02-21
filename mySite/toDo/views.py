from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, ToDoList, SingleTask
import hashlib

# Create your views here.

def main(request):
    return render(request, 'toDo/main.html', None)


def login(request):
    # toDo CHECK IF THERE IS A LOGGIN COOKIE SO IT IS NOT NEEDED TO DO THE CHECK IN
    return render(request, 'toDo/logIn.html', None)


def register (request, problem=0):
    return render(request, 'toDo/register.html', {'problem':problem})


def registrationInfo(request):
    if request.POST['password'] != request.POST["password2"]:
        return render(request, 'toDo/register.html', {'problem': 2})

    if User.objects.filter(user = request.POST['username']).count() >= 1:
        return render(request, 'toDo/register.html', {'problem': 1})

    if User.objects.filter(email=request.POST['email']).count() >= 1:
        return render(request, 'toDo/register.html', {'problem': 2})

    else:
        print("We add the user")
        User.objects.create(user=request.POST['username'], password=hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest(), email=request.POST['email'], name=request.POST["name"])
        return redirect("login")


def identifing (request):
    try:
        global usuari
        global remember

        email = request.POST['email']
        password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
        usuari = User.objects.get(email=email, password=password)

        if 'rememberMe' in request.POST and request.POST['rememberMe'] == 'on':
            remember = True

        else:
            remember = False

        return redirect(personalSite)

    except:
        print("You need to register first")
        return render(request, 'toDo/logIn.html', None)



def personalSite(request):
    try:
        global usuari
        list = usuari.todolist_set.all()
        empty = len(list) == 0
        return render(request, 'toDo/personalSite.html', {'name':usuari, 'list':list, 'empty':empty})

    except:
        return render(request, 'toDo/logIn.html', None)


def specificList (request):
    try:
        #make sure that chose_list returns only one
        if 'chosen_list' in request.POST:
            global chosen
            chosen = request.POST['chosen_list']

        if 'Delete' in request.POST:
            ToDoList.objects.get(title=chosen).delete()
            return redirect('personalSite')

        else:
            try:
                list = ToDoList.objects.get(title=chosen)
                tasks = list.singletask_set.all()

            except:
                return redirect(personalSite)

            return render(request, 'toDo/specificList.html', {'list':list, 'tasks':tasks})

    except:
        return render(request, 'toDo/logIn.html', None)


def processChanges (request):
    try:
        #those that are marked have to be marked as completed
        list = ToDoList.objects.get(title=chosen)
        tasks = list.singletask_set.all()
        for e in tasks:
            t = list.singletask_set.get(task=e.task)
            if e.task in request.POST and request.POST[e.task] == 'on': #we permenently select
                t.completed = True
            else:
                t.completed= False
            t.save()

        return redirect('specificList')

    except:
        return render(request, 'toDo/logIn.html', None)


def addTask(request):
    try:
        l = ToDoList.objects.get(title=chosen)
        if 'newTask' in request.POST and request.POST['newTask'] != '':
            SingleTask.objects.create(task=request.POST['newTask'], completed=False, list = l)

        return redirect('specificList')

    except:
        return render(request, 'toDo/logIn.html', None)

def addList(request):
    try:
        if 'newList' in request.POST and request.POST['newList'] != '':
            ToDoList.objects.create(title=request.POST['newList'], owner = usuari)
        return redirect('personalSite')
    except:
        return render(request, 'toDo/logIn.html', None)


def logout(request):
    global usuari
    usuari = None
    return redirect('main')