# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib.messages import error,success
from django.contrib import messages
import bcrypt
from django.shortcuts import render,redirect
from .models import *

# Create your views here.



def index(request):
    if 'id' in request.session:
        context={
        'person':User.objects.exclude(id=request.session['id']),
        'unique':User.objects.get(id=request.session['id']),
        'friendship':FriendShip.objects.exclude(friend=request.session['id'])
        }
        return render (request, 'friend/user.html',context)
    else:
        return render(request, 'friend/index.html')

def create(request):
    errors=User.objects.validate(request.POST)
    if len(errors):
        for err in errors:
            error(request,err)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw((request.POST['pass'].encode()), bcrypt.gensalt(5))
        User.objects.create(name=request.POST['name'],
        alias=request.POST['alias'],email=request.POST['email'],
        password=hashed)
        messages.success(request,'Shit has been added')
        return redirect('/')

def remove(request,number):
    a=FriendShip.objects.filter(id=number)
    a.delete()
    return redirect('/')

def login(request):
    errors=User.objects.login(request.POST)
    if len(errors):
        for err in errors:
            error(request,err)
            return redirect('/')
    else:
        check=User.objects.filter(email=request.POST['lemail'])
        if len(check)>0:
            Users=check[0]
            if not bcrypt.checkpw(request.POST['lpass'].encode(), Users.password.encode()):
                messages.error(request,"Password or Login Are INCORRECT!")
                return redirect('/')
            request.session['id']=Users.id
            print User.objects.all()
            context={
            'person':User.objects.all(),
            'unique':User.objects.get(id=request.session['id'])
            }
            return redirect('/')
        else:
            messages.error(request,'Password or Login is wrong as FUCK!')

        return redirect ('/')
def add(request,number):
    a=User.objects.filter(id=number)[0]
    b=User.objects.filter(id=request.session['id'])[0]
    FriendShip.objects.create(creator=b,friend=a)
    return redirect('/')



def logout(request):
    request.session.clear()
    return redirect('/')
