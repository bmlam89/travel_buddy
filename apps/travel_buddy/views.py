# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request,"index.html")

def registration(request):
    errors = User.objects.is_valid(request.POST)
    
    #len errors = 0 means all registration input was valid
    if len(errors) == 0:

        #check to see if username is taken
        if len(User.objects.filter(username=request.POST["username"])) == 0:
            new_user = User.objects.create(name=request.POST["name"],username=request.POST["username"],password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            request.session["id"] = new_user.id
            return redirect("/travels")
        else:
            messages.add_message(request, messages.ERROR, "Username is already taken!")
            return redirect("/main")
    else:
        #print "INSIDE ERRORS"
        for key in errors:
            messages.add_message(request, messages.ERROR, errors[key])
        return redirect("/main")

def login(request):
    all_users = User.objects.all()
    for user in all_users:
        if user.username == request.POST["username"] and bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
            request.session['id'] = user.id
            return redirect("/travels")
    messages.add_message(request, messages.ERROR, "Invalid username or password")
    return redirect("/main")

def logout(request):
    request.session.clear()
    return redirect("/main")



def travels(request):
    your_trips = Trip.objects.filter(user_id=request.session["id"])

    #user = User.objects.get(id=request.session["id"])
    #shared_trips = user.shared_trips.all()
    #your_trips = your_trips | shared_trips
    all_trips = Trip.objects.exclude(user_id=request.session["id"])
    #shared_trips = Trip.shared_users.all()
    context = {
        "user":User.objects.get(id=request.session["id"]),
        "your_trips":your_trips,
        "all_trips":all_trips,
        "user":User.objects.get(id=request.session["id"])
    }
    return render(request,"travels.html",context)


def add(request):
    return render(request,"add_plan.html")

def submit(request):
    errors = Trip.objects.valid_trip(request.POST)
    if len(errors) == 0:
        new_trip = Trip.objects.create(destination=request.POST["destination"],departure_date=request.POST["from"],return_date=request.POST["to"],desc=request.POST["desc"],user=User.objects.get(id=request.session["id"]))
        return redirect("/travels")
    else:
        for key in errors:
            messages.add_message(request, messages.ERROR, errors[key])
        return redirect("/travels/add")

def destination(request,id):
    trip = Trip.objects.get(id=id)
    others = trip.shared_users.all()
    context = {
        "trip":trip,
        "others":others
    }
    return render(request,"destination.html",context)

def join(request,id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session["id"])
    user.shared_trips.add(trip)
    new_trip = Trip.objects.create(destination=trip.destination,departure_date=trip.departure_date,return_date=trip.return_date,desc=trip.desc,user=User.objects.get(id=request.session["id"]))
    return redirect("/travels")