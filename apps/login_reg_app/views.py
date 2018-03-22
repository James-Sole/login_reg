# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import messages
from models import *
import bcrypt
def index(request):
	return render(request, "login_reg_app/index.html")
def login(request, methods = ['POST']):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/')
    request.session['id']= User.objects.get(email = request.POST['email']).id
    request.session['status']= 'logged in'
    return redirect('/success/{}'.format(request.session["id"]))

def register(request, methods = ['POST']):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/')
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = password)
    request.session['id']= User.objects.last().id
    request.session['status']= 'registered'
    return redirect('/success/{}'.format(request.session["id"]))

def success(request, id):
    if 'id' in request.session:
        context = {
            'first_name': User.objects.get(id = id).first_name,
            'last_name': User.objects.get(id = id).last_name,
        }
        return render(request, "login_reg_app/success.html", context)
    return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
