from django.shortcuts import render, redirect
from .models import User, ToDoList, SingleTask
import hashlib
from random import randint

# Import smtplib for the actual sending function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# Create your views here.

def main(request):
    return render(request, 'toDo/main.html', None)


def login(request):
    return render(request, 'toDo/logIn.html', None)


def register (request, problem=0):
    return render(request, 'toDo/register.html', {'problem':problem})


def registrationInfo(request):
    if request.POST['password'] != request.POST["password2"]:
        return render(request, 'toDo/register.html', {'problem': 2})

    if User.objects.filter(email=request.POST['email'],confirmed=False).count() >=1:
        User.objects.get(email=request.POST['email'], confirmed=False).delete()


    if User.objects.filter(user = request.POST['username']).count() >= 1:
        return render(request, 'toDo/register.html', {'problem': 1})

    if User.objects.filter(email=request.POST['email']).count() >= 1:
        return render(request, 'toDo/register.html', {'problem': 2})


    else:
        sendEmail(request.POST['email'])   #we send mail for confirmation
        User.objects.create(user=request.POST['username'], password=hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest(), email=request.POST['email'], name=request.POST["name"])
        return render(request, 'toDo/confirmationSent.html', None)



def sendEmail(receiver_email):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "confirmation.toDo@gmail.com"
    password = 'iavm2umr'

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    html = """\
    <html>
      <body>
        <p>
            Hello dear new user,<br>
            We would like to welcome you to our toDo platform that will bring order into your life by enabling you
            to keep track of your pending tasks as well as the completed ones.<br><br>
            We wanted to remind you that in case of having any doubt in any functionality, please do not hesitate
            to contact us so we can help you as soon as possible.<br><br>

            Before so, and for security porpuses, we need you to confirm your account.<br>
        </p>
        <p>Please click on the following link <a href="localhost:8000/toDo/confirmationProcess">Click_here</a></p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl._create_unverified_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def identifing (request):
    try:
        global usuari
        global remember

        email = request.POST['email']
        password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
        usuari = User.objects.get(email=email, password=password, confirmed=True)

        if 'rememberMe' in request.POST and request.POST['rememberMe'] == 'on':
            remember = True

        else:
            remember = False

        return redirect(personalSite)

    except:
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


def contact(request):
    return render(request, 'toDo/contact.html', None)


def confirmation(request):
    p = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
    if User.objects.get(email=request.POST['email'], password=p):
        u = User.objects.get(email=request.POST['email'], password=p)
        u.confirmed = True
        u.save()
        return render(request, 'toDo/confirmation.html', None)

    else:
        return redirect(confirmationProcess)


def confirmationProcess(request):
    return render(request, 'toDo/confirmationProcess.html', None)