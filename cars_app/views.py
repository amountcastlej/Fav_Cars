from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def register(request): 
    if request.method == "POST": 
        errors = User.objects.Registration_Validator(request.POST) 
        if len(errors) != 0: 
            for key, value in errors.items(): 
                messages.error(request, value) 
            return redirect('/') 
        else: 
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email = request.POST['email'], password = hashed_pw) 
            request.session['user_id'] = new_user.id 
            return redirect('/cars')  
    else:
        return redirect('/')

def login(request): 
    if request.method == "POST": 
        errors = User.objects.Login_Validator(request.POST) 
        if len(errors) > 0: 
            for key, value in errors.items(): 
                messages.error(request, value) 
            return redirect('/') 
        this_user = User.objects.filter(email = request.POST['email']) 
        request.session['user_id'] = this_user[0].id 
        return redirect('/cars') 
    return redirect('/')

def cars(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    all_users = User.objects.all()
    car_likes = Car.objects.all().order_by('-users_who_like')
    context = {
        'this_user' : this_user[0],
        'all_cars': Car.objects.all().order_by('-created_at'),
        'all_users': all_users,
    }
    return render(request, 'cars.html', context)

def add(request):
    if request.method == "POST":
        errors = Car.objects.Car_Validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/cars')
        else:
            user = User.objects.get(id=request.session['user_id'])
            car = Car.objects.create(make=request.POST['make'], model=request.POST['model'], uploaded_by = user)
            # car.users_who_like.add(user)
            return redirect('/cars')
    else:
        return redirect('/cars')

def car(request, car_id):
    one_car = Car.objects.get(id=car_id)
    this_user = User.objects.get(id=request.session['user_id'])
    
    context = {
        'car': one_car,
        'this_user': this_user
    }
    return render(request, 'car.html', context)

def update(request, car_id):
    if request.method == "POST":
        car = Car.objects.get(id=car_id)
        car.make = request.POST['make']
        car.model = request.POST['model']
        car.save()
    return redirect(f'/cars/{car.id}')

def delete(request, car_id):
    car = Car.objects.get(id=car_id)
    car.delete()
    return redirect('/cars')

def like(request, car_id):
    user = User.objects.get(id=request.session['user_id'])
    car = Car.objects.get(id=car_id)
    user.liked_cars.add(car)
    return redirect('/cars')

def user(request, user_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'cars_uploaded': Car.objects.filter(id=request.session['user_id'])
    }
    return render(request, 'user.html', context)

def logout(request): 
    request.session.flush() 
    return redirect('/')
