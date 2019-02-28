from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('/login', views.login, name="login"),
    #localhost:8000/toDo/login

    path('/register', views.register, name="register"),
    #localhost:8000/toDo/register

    path('/register/registrationInfo', views.registrationInfo, name='registrationInfo'),

    path('', views.main, name="main"),
    #localhost:8000/toDo

    path('/identifing', views.identifing, name='identifing'),


    path('/personalSite', views.personalSite, name='personalSite'),

    path('/personalSite/SpecificList', views.specificList, name='specificList'),

    #this two following url are accesed but will directly redirect to the previous so it will not show up for the user
    path('/personalSite/SpecificList/ProcessChanges', views.processChanges, name='processChanges'),


    path('/personalSite/SpecificList/AddTask', views.addTask, name='addTask'),


    path('/personalSite/SpecificList/AddList', views.addList, name='addList'),

    path('/logout', views.logout, name='logout'),

    path('/confirmation', views.confirmation, name="confirmation"),

    path('/confirmationProcess', views.confirmationProcess, name="confirmationProcess"),

    path('/contact', views.contact, name='contact'),

]
