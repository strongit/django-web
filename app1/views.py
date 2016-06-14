# _*_ coding: utf-8 _*_
from django.shortcuts import render


# Create your views here.

def home(request):
    TutorList = ["hosts", "mysql", "bootstrap"]
    return render(request, 'home.html', {'TutorList': TutorList})

def hosts(request):
    return render(request, 'hosts.html')