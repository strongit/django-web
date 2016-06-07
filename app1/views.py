# _*_ coding: utf-8 _*_
from django.shortcuts import render


# Create your views here.

def home(request):
    TutorList = ["django", "mysql", "bootstrap"]
    for i in TutorList:
        return render(request, 'home.html',  {"%s.html"}) %i