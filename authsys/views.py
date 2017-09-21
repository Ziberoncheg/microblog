from django.shortcuts import render, redirect
from authsys.models import MyUser
from django.contrib.auth import authenticate,logout, login as auth_login
import random
import datetime
from django.core.mail import send_mail
# Create your views here.


def loginpage(request):

    return render(request, "loginpage.html", context=None)

#@csrf_exempt
def register(request):
    args = {}
    try:
        d1_1 = int(request.POST.get('YY', ''))
        d1_2 = int(request.POST.get('MM', ''))
        d1_3 = int(request.POST.get('DD', ''))
        user = MyUser.objects.create_user(request.POST.get('email', ''),datetime.date(d1_1,d1_2,d1_3),
                                          request.POST.get('country', ''),request.POST.get('city', ''),
                                          request.POST.get('password', ''))
        ua_code = "%s" % random.randrange(1,9999999999999999999999999999)
        user.activation_code = ua_code
        user.date_of_birth =datetime.date(d1_1,d1_2,d1_3)
        user.city = request.POST.get('city', '')
        user.country = request.POST.get('country', '')
        user.save()
        args['message'] = "New user created. Please confirm your email adress"
        send_mail(
            'Activation account',
            'For activation your account click at link https://ziberon.herokuapp.com/auth/activation/%s' % ua_code,
            'from@example.com',
            ['%s' % request.POST.get('email', '')],
            fail_silently=False,
        )
        return render(request, "loginpage.html", args)
    except:
       args['message'] = "User is already registered or incorrectly filled in fields"
       return render(request,"loginpage.html", args)




def login(request):
    user = authenticate(username=request.POST.get('email', ''), password=request.POST.get('password', ''))

    if user is not None:
        auth_login(request, user)

        return redirect('/')
    else:
        return render(request,"loginpage.html", {'message': 'incorrect login or password'})


def logout_v(request):
    logout(request)
    return render(request, "loginpage.html", {'message': 'Logout'})


def user_activation(request, code):
    try:
        user = MyUser.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = "0000----0000----0000"
        user.save()
        return render(request, "loginpage.html", {'message': 'User is active. Lets log in'})
    except:
        return render(request, "loginpage.html", {'message': 'User is active or invalid link'})
