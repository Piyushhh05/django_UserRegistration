from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from random import randint

# Create your views here.

def register(request):
    EUFO = UserForm()
    EPFO = ProfileForm()
    d = {'EUFO':EUFO,'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid():
            MUFDO = UFDO.save(commit=False)
            pw = UFDO.cleaned_data.get('password')
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO = PFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()
            message=f"Hello {UFDO.cleaned_data.get('first_name')} Your Registration Is done Successfully \n\n Thanks and regards\n\n Team Piyush"
            email=UFDO.cleaned_data.get('email')
            send_mail(
                'Registration Is Done',
                message,
                'piyushgamechanger5@gmail.com',
                [email],
                fail_silently=False
            )
            return HttpResponse('User Registration is done successfully !!!')
        return HttpResponse('Invalid Data ...')
    return render(request, 'register.html', d)


def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('un')
        password=request.POST.get('pw')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return render(request,'home.html',{'user':user})
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')


@login_required
def user_profile(request):
    try:
        un=request.session['username']
        UO=User.objects.get(username=un)
        d={'UO':UO}
        request.session.modified=True
        return render(request,'user_profile.html',d)
    except:
        return render(request,'user_login.html')
    

def home(request):
     request.session.modified=True
     return render(request,'home.html')


def changepassword(request):
    if request.method == 'POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            otp= randint(100000,999999)
            request.session['pw']=pw
            request.session['otp']=otp
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            email=UO.email
            send_mail(
                "RE:- OTP for change the Password",
                f"OTP for change the Password is: {otp} ",
                'piyushgamechanger5@gmail.com',
                [email],
                fail_silently=False
            )
            return render(request,'otp.html')
        return HttpResponse('Password Not Verified')
    return render(request,'changepassword.html')


def otp(request):
    if request.method == 'POST':
        UOTP=request.POST.get('otp')
        GOTP=request.session.get('otp')
        print(GOTP)
        if UOTP==str(GOTP):
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            pw=request.session.get('pw')
            UO.set_password(pw)
            UO.save()
            return HttpResponse('Password Updated !!!')
        return HttpResponse('Invalid OTP...')
    return render(request,'otp.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request,'home.html')


def forgotpassword(request):
    if request.method == 'POST':
        un=request.POST.get('un')
        UO=User.objects.get(username=un)
        if UO:
            otp= randint(100000,999999)
            request.session['otp']=otp
            request.session['username']=un
            email=UO.email
            send_mail(
            'OTP for forgot password',
            f'OTP for the forgot password: {otp}',
            'piyushgamechanger5@gmail.com',
            [email],
            fail_silently=False
            )
            return render(request,'forgotpasswordotp.html')
        return HttpResponse('Username Not Verified')
    return render(request,'forgotpassword.html')


def forgotpasswordotp(request):
    if request.method == 'POST':
        UOTP=request.POST.get('otp')
        GOTP=request.session.get('otp')
        if UOTP==str(GOTP):
            return render(request,'updatepassword.html')
        return HttpResponse('Invalid OTP')
    return render(request,'fogotpasswordotp.html')


def updatepassword(request):
    if request.method == 'POST':
        pw=request.POST.get('pw')
        cpw=request.POST.get('cpw')
        if pw==cpw:
            un=request.session.get('username')
            UO=User.objects.get(username=un)
            UO.set_password(pw)
            UO.save()
            return render(request,'user_login.html')
        return HttpResponse('Password Not Matched')
    return render(request,'updatepassword.html')
    
    