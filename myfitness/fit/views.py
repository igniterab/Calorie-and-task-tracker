from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import auth
from datetime import datetime, date
import requests

# Create your views here.


def index(request):
    option = False
    try:
        if request.session.has_key('username'):
            option = True
        else:
            option = False
    except:
        return HttpResponse('Error 404')

    return render(request, 'index.html', {'option': option})


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first']
        last_name = request.POST['last']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        age = request.POST['age']
        weight = request.POST['weight']
        height = request.POST['height']
        excercise = request.POST['excercise']
        gender = request.POST['radio-group']
        print(first_name, last_name, email, pass1, pass2,
              weight, height, age, excercise, gender)
        if pass1 == pass2:
            try:
                email = request.POST['email']
                user = User.objects.filter(email=email)
                if len(user) == 0:
                    raise User.DoesNotExist
                return render(request, 'user/signup.html', {'msg': 'Email already exists 🔑', 'c': 'red'})
            except:
                if gender:
                    BMR = 66.47 + (13.75 * int(weight)) + \
                        (5.003 * int(height)) - (6.755 * int(age))
                BMR = 655.1 + (9.563 * int(weight)) + \
                    (1.85 * int(height)) - (4.676 * int(age))

                # print(BMR)
                if excercise == '0':
                    BMR = BMR * 1.05
                if excercise == '1':
                    BMR = BMR * 1.375
                if excercise == '2':
                    BMR = BMR * 1.55
                if excercise == '3':
                    BMR = BMR * 1.725
                if excercise == '4':
                    BMR = BMR * 1.9

                new_user = User.objects.create_user(
                    first_name=first_name, last_name=last_name, email=email, username=email, password=pass1)
                new_user.save(False)
                new_pro = Profile(username=new_user, age=age, height=height, weight=weight,
                                  profile_img="", excercise_status=excercise, calorie_needed=BMR)
                new_user.save()
                new_pro.save()
                person_register = person(person=new_user)
                person_register.save()
                return redirect('signin')
                # return render(request, 'register.html', {"error": 'Account Created 🔑', 'c': 'green'})
                # return render(request , 'register.html')
        else:
            return render(request, 'register.html', {'error': 'Password should match'})
    return render(request, 'register.html')


def signin(request):

    if request.method == 'POST':
        try:
            # Check User in DB
            uname = request.POST['email']
            pwd = request.POST['pass1']
            print(uname, pwd)
            User.objects.get(username=uname)
            user_authenticate = auth.authenticate(username=uname, password=pwd)
            if user_authenticate is not None:
                auth.login(request, user_authenticate)
                request.session['username'] = uname
                print('Successfully Login')
                return redirect('/')
            else:
                print('Login Failed')
                return render(request, 'login.html', {"error": "Invalid Credentials ❌", 'c': 'red'})
        except:
            return render(request, 'login.html', {'error': 'User not exists.', 'c': 'red'})
    return render(request, 'login.html')


def profile(request):
    option = False
    try:
        if request.session.has_key('username'):
            option = True
        else:
            option = False
    except:
        return HttpResponse('Error 404')
    data = User.objects.get(username=request.session['username'])
    profile = Profile.objects.get(username=data)
    print(data, profile)
    return render(request, 'profile.html', {'option': option, 'data': data, 'profile': profile})


def calorie(request):
    option = False

    if request.session.has_key('username'):
        option = True
        user = User.objects.get(username=request.session['username'])
        print(user)
        item_list = Food.objects.filter(user=user)
        print(item_list)
        if request.method == "POST":
            try:
                dnow = Food.objects.filter(user=user)
                if (dnow[0].date != datetime.today().date()):
                    dnow.delete()
            except:
                pass
            entry = Food(user=user, title=request.POST['food'])
            print(entry)
            entry.save()
            sum_ = 0

            def search(item):
                # item = request.POST['food']
                print("🚀", item)
                headers = {
                    'x-app-id': "ff0ccea8",
                    'x-app-key': "605660a17994344157a78f518a111eda",
                    'x-remote-user-id': "7a43c5ba-50e7-44fb-b2b4-bbd1b7d22632",
                    'Content-Type': "application/x-www-form-urlencoded",
                }
                url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
                body = {
                    'query': item,
                    'timezone': 'US/Eastern',
                }
                response = requests.request(
                    "POST", url, data=body, headers=headers)
                data = response.json()
                cals = data['foods'][0]['nf_calories']
                print(response, cals, item)
                return cals

            # Cals Needed
            x = Profile.objects.get(username=user)

            for i in item_list:
                food = i.title
                sum_ += search(food)

            sum_ = (sum_/x.calorie_needed)*100
            sum_ = int(sum_)
            print("Sum=", sum_)
            x = int(x.calorie_needed)
            return render(request, 'calorie.html', {'option': option, 'item_list': item_list, 'sum_': sum_, 'x': x})

        else:
            sum_ = 0

            def search(item):
                # item = request.POST['food']
                print("🚀", item)
                headers = {
                    'x-app-id': "ff0ccea8",
                    'x-app-key': "605660a17994344157a78f518a111eda",
                    'x-remote-user-id': "7a43c5ba-50e7-44fb-b2b4-bbd1b7d22632",
                    'Content-Type': "application/x-www-form-urlencoded",
                }
                url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
                body = {
                    'query': item,
                    'timezone': 'US/Eastern',
                }
                response = requests.request(
                    "POST", url, data=body, headers=headers)
                data = response.json()
                cals = data['foods'][0]['nf_calories']
                print(response, cals, item)
                return cals

            # Cals Needed
            x = Profile.objects.get(username=user)

            for i in item_list:
                food = i.title
                sum_ += search(food)

            sum_ = (sum_/x.calorie_needed)*100
            sum_ = int(sum_)
            print("Sum=", sum_)
            x = int(x.calorie_needed)
            return render(request, 'calorie.html', {'option': option, 'item_list': item_list, 'sum_': sum_, 'x': x})

    return HttpResponse('Error 404')


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('/')


def edit(request, id, user):
    try:
        mark = True
        obj = personTask.objects.get(id=id)
        print(obj)
        return render(request, 'edit.html', {'mark': mark, 'object': obj})
    except:
        return HttpResponse("kuch gadbad hui h...")


def delete(request, id, user):
    try:
        user = User.objects.get(username=request.session['username'])
        kk = personTask.objects.get(id=id)
        kk.delete()
        return redirect('tasks')
    except:
        return HttpResponse("aukat se jada ki kosis na kro...")


def check(request, id, user):
    user = User.objects.get(username=request.session['username'])
    kk = personTask.objects.get(id=id)
    mk = person.objects.get(person=user)
    if mk.points == None:
        mk.points = 0
        mk.save()
    if kk.action == False:
        kk.action = True
        kk.save()
    total_task = personTask.objects.filter(
        user=user, date=date.today(), action=True)
    print(total_task)
    counts = len(total_task)
    if counts >= 1:
        print("pahuch gya")
        mk.points = counts*10
        mk.save()
    return redirect('tasks')


def edit_save(request, obj):
    if request.method == "POST":
        name = request.POST.get('task')
        date = request.POST.get('date')
        time = request.POST.get('time')
        kk = personTask.objects.get(id=obj)
        kk.task = name
        kk.date = date
        kk.time = time
        kk.save()
    return redirect('tasks')


def get_data(request):
    if request.method == "POST":
        name = request.POST.get('task')
        date = request.POST.get('date')
        time = request.POST.get('time')
        main = User.objects.get(username=request.session['username'])
        obj = personTask.objects.create(
            user=main, task=name, date=date, time=time)
        data = personTask.objects.filter(user=main)
        return redirect('tasks')


def leaderboard(request):
    option = False
    try:
        if request.session.has_key('username'):
            user = User.objects.get(username=request.session['username'])
            per = person.objects.get(person=user).points
            print(per)
            mk = person.objects.all()
            print(mk)
            def func(x): return x.points
            data = sorted(mk, key=func, reverse=True)
            print(data)
            option = True
        else:
            option = False
    except:
        return HttpResponse('Error 404')

    return render(request, 'leaderboard.html', {'option': option, 'you': per, 'datas': data})


def tasks(request):
    option = False

    if request.session.has_key('username'):
        user = User.objects.get(username=request.session['username'])
        print(user)
        # print(personTask.objects.all())
        data = personTask.objects.filter(date=date.today(), user=user)
        print(data)
        point = person.objects.get(person=user).points
        print(point)

        option = True
    else:
        option = False

    return render(request, 'tasks.html', {'option': option, 'data': data, 'points': point})
