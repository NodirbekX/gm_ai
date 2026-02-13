from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

# REGISTER
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import CustomUser


def register_view(request):
    if request.method == "POST":

        username = request.POST.get("login")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        passport_id = request.POST.get("passport_id")
        permanent_address = request.POST.get("permanent_address")
        password = request.POST.get("password")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu login band!")
            return redirect("register")

        CustomUser.objects.create(
            username=username,
            full_name=full_name,
            phone=phone,
            passport_id=passport_id,
            permanent_address=permanent_address,
            password=make_password(password)
        )

        messages.success(request, "Ro'yxatdan o'tdingiz! Login qiling.")
        return redirect("login")

    return render(request, "register.html")


# LOGIN
def login_view(request):
    if request.method == "POST":

        username = request.POST.get("login")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Login yoki parol noto‘g‘ri!")

    return render(request, "login.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("home")

#all cars
def cars_list(request):
    return render(request, 'cars_list.html')

#Captiva
def captiva_detail(request):
    return render(request, 'models/captiva.html')

def tracker_detail(request):
    return render(request, 'models/tracker.html')

def onix_detail(request):
    return render(request, 'models/onix.html')

def captiva_config(request):
    return render(request, 'models/captiva_config.html')

#buy view

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import FileResponse
from docx import Document
import os
from datetime import datetime


@login_required
def buy_car(request):
    if request.method == "POST":

        user = request.user
        model = request.POST.get("model")

        # Create document
        document = Document()

        document.add_heading('AVTOMOBIL SOTIB OLISH SHARTNOMASI', level=1)

        document.add_paragraph(f"Sana: {datetime.now().strftime('%d.%m.%Y')}")
        document.add_paragraph("")

        document.add_paragraph(f"Xaridor: {user.full_name}")
        document.add_paragraph(f"Passport ID: {user.passport_id}")
        document.add_paragraph(f"Telefon: {user.phone}")
        document.add_paragraph(f"Manzil: {user.permanent_address}")
        document.add_paragraph("")
        document.add_paragraph(f"Sotib olinayotgan avtomobil: Chevrolet {model}")
        document.add_paragraph("")
        document.add_paragraph("Tomonlar yuqoridagi ma’lumotlarga asosan shartnoma tuzdilar.")

        # Save file
        filename = f"{user.username}_{model}_{datetime.now().timestamp()}.docx"
        filepath = os.path.join(settings.MEDIA_ROOT, "contracts", filename)

        document.save(filepath)

        return FileResponse(open(filepath, 'rb'), as_attachment=True)

    return redirect("home")
