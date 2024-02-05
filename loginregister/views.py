from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from .models import UserDetail
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# def userregister(request):
#     message = None
#     msg = None
#     em = None
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         phone_number = request.POST['phone_number']
#         password = request.POST['password']
#         cpassword = request.POST['cpassword']
#
#         if password == cpassword:
#             if UserDetail.objects.filter(email=email).exists():
#                 em = "email already taken"
#
#                 return render(request, 'userreg.html', {'em': em})
#
#             else:
#                 user1 = User.objects.create_user(username=name, email=email, password=password)
#                 user1.save()
#
#                 # Create a corresponding UserDetail object
#                 user_detail = UserDetail(name=name, email=email, phone_number=phone_number, password=password)
#                 user_detail.save()
#
#                 messages.success(request, "User registration successful. You can now log in.")
#                 return redirect('userlogin')
#                 message = "User registration successful."
#
#         # Redirect to a success page after registrations
#         else:
#             msg = "password not maching"
#             return render(request, 'userreg.html', {'msg': msg})
#
#     return render(request, 'userreg.html', {'message': message})  # This assumes you have a registration form template
#


def userregister(request):
    message = None
    msg = None
    em = None

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # Validate password length using Django's built-in validator
        try:
            validate_password(password)
        except ValidationError as e:
            msg = e.messages[0]  # Show the first error message
            return render(request, 'userreg.html', {'msg': msg})

        if password == cpassword:
            if UserDetail.objects.filter(email=email).exists():
                em = "Email already taken"
                return render(request, 'userreg.html', {'em': em})

            else:
                user1 = User.objects.create_user(username=name, email=email, password=password)
                user1.save()

                # Create a corresponding UserDetail object
                user_detail = UserDetail(name=name, email=email, phone_number=phone_number, password=password)
                user_detail.save()

                messages.success(request, "User registration successful. You can now log in.")
                return redirect('userlogin')
                message = "User registration successful."

        else:
            msg = "Passwords do not match"
            return render(request, 'userreg.html', {'msg': msg})

    return render(request, 'userreg.html', {'message': message})


# Add any other views you may need
def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # print(email,password)
        # print(type(password))
        username = User.objects.get(email=email.lower()).username
        user2 = auth.authenticate(username=username, password=password)
        print(user2)
        if user2 is not None:
            auth.login(request, user2)
            # Redirect to a success page or the user's dashboard
            return redirect('userindex')  # Replace 'dashboard' with the actual URL name for the user's dashboard

        else:
            # Authentication failed, show an error message
            error_message = "Invalid email or password."
            return render(request, 'userlogin.html', {'error_message': error_message})

    return render(request, 'userlogin.html')


def index(request):
    return render(request, 'index.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def contactus(request):
    return render(request, 'contactus.html')


def tire(request):
    return render(request, 'tire.html')


def services(request):
    return render(request, 'services.html')
