from django.shortcuts import render, redirect
from .models import *
from django.contrib.messages import error
#import bycrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.user_validator(request.POST)
    
    if errors:
        for e in errors:
            error(request, e)
        return redirect('/')
    else:
        user = User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'],password=request.POST['password'])
        request.session['userID'] = user.id 
        request.session['name'] = user.first_name
        return redirect('/dashboard')

def user_login(request):
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['password']:
            request.session['userID'] = logged_user.id 
            request.session['name'] = logged_user.first_name 
            return redirect('/dashboard')
        elif logged_user.password != request.POST['password']:
            error(request, "Incorrect password")
        return redirect ('/')
    else:
        error(request, "This email has not been registered.")
        return redirect('/')

def show_wall(request):
    if 'userID' not in request.session:
        return redirect('/')
    else:
        context = {
            'games': Game.objects.all(),
            'current_user': User.objects.get(id=request.session['userID']) 

        }
    return render(request, 'blogwall.html', context)

def new_game(request):
    return render(request, 'add.html')

def add_game(request):
    errors = Game.objects.post_validate(request.POST)

    if errors:
        for e in errors:
            error(request, e)
        return redirect('/new')
    else:
        user = User.objects.get(id = request.session['userID'])
        Game.objects.create(title=request.POST['gtitle'], description=request.POST['desc'], rating=request.POST['grating'], platform=request.POST['platform'], created_by=user)
        return redirect('/dashboard')

def one_game(request,id):
    context = {
        'game': Game.objects.get(id=id)
    }
    return render(request, 'add.html', context)

def post_comment(request, id):
    poster = User.objects.get(id=request.session['userID'])
    message = Game.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], creator=poster, wall_message=message)
    return redirect('/dashboard')

def update(request, id):
    errors = Game.objects.post_validate(request.POST)

    if errors:
        for e in errors:
            error(request, e)
        return redirect(f'/show_one/{id}')
    else:
        game = Game.objects.get(id=id)
        game.title = request.POST['gtitle']
        game.description = request.POST['desc']
        game.rating = request.POST['grating']
        game.save()
    return redirect('/dashboard')

def delete(request,id):
    game = Game.objects.get(id=id)
    game.delete()
    return redirect('/dashboard')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/dashboard')

def sign_out(request):
    request.session.flush()
    return redirect('/')