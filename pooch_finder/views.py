from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.db import IntegrityError
from .models import Breed, Dog_Type, Age_Cat, Gender, Picture, Location, Ad_Item, State
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings as conf_settings
import os
import sqlite3
from datetime import datetime
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator


# Create your views here.

#login page
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username:
            return render(request, "users/login.html", {"message": "Must provide username."})
        if not password:
            return render(request, "users/login.html", {"message": "Must provide password."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        request.session.clear()
        return render(request, "users/login.html", {"message": None})