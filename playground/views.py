from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Room, Topic, Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm, MessageForm, UserForm
from django.db.models import Q

# Create your views here.

# rooms = [
#         {'id': 1, 'name': "Django development tutorial"},
#         {'id': 2, 'name': "Python with Mosh"},
#         {'id': 3, 'name': "Design course"}
# ]

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            # pwd = User.objects.get(password=password)
        except:
            messages.error(request, 'User does not exist!')
        
        # returns user object that matches this credentials (if exists)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Adds the session in the database and in the browser
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist!')
    
    if request.user.is_authenticated:
        return redirect('home')

    context = {'page':page}
    return render(request, 'playground/login_register.html', context)

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
    context = {'form':form}
    return render(request, 'playground/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')     

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q) | 
        Q(host__username__icontains=q))
    topics = Topic.objects.all()[0:5]
    topics_count = topics.count()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages, 'topics_count': topics_count}
    return render(request, 'playground/home.html', context)
    
def room(request, pk):
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i

    room=Room.objects.get(id=pk)
    room_messsages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        redirect('room', room.id)
        participants = room.participants.add(request.user)

    context = {'room': room, 'room_messages': room_messsages, 'participants': participants}
    return render(request, 'playground/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()

    context = {'user': user, 'topics': topics, 'rooms': rooms, 'room_messages': room_messages}
    return render(request, 'playground/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host=request.user
        #     # room.participants=request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics':topics}
    return render(request, 'playground/room_form.html', context)

# @login_required(login_url='login')
# def updateRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance=room)
#     topics = Topic.objects.all()

#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!')

#     if request.method == 'POST':
#         topic_name=request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name=topic_name)
#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')
#     # else:
#     #     return HttpResponse('Failed')

#     context = {'form': form, 'topics': topics, 'room': room}
#     return render(request, 'playground/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # form = RoomForm(instance=room)
    name = room.name
    topic = room.topic
    description = room.description
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    # else:
    #     return HttpResponse('Failed')

    context = {'name':name,'description':description,'topics': topics, 'room': room}
    return render(request, 'playground/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    # form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'playground/delete.html', {'obj':room})

def createUser(request):
    form = RoomForm()
    if request.method == 'POST':
        form.RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'playground/home.html', {'form',form})

# def updateMessage(request, pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance=room)

#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!')

#     if request.method == 'POST':
#         form = RoomForm(request.POST, instance=room)
#         if form.is_valid:
#             form.save()
#             return redirect('home')
#     context = {'form': form}
#     return render(request, 'playground/room_form.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    # form = RoomForm(instance=room)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'playground/delete.html', {'obj':message})
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'playground/update-user.html', {'form': form})

# @login_required(login_url='login')

# def deleteRecent(request, pk):
#     message = Message.objects.get(id=pk)
#     # form = RoomForm(instance=room)

#     if request.method == 'POST':
#         message.delete()
#         return redirect('home')

#     return render(request, 'playground/delete.html', {'obj':message})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains=q))

    return render(request, 'playground/topics.html', {"topics":topics})

def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains=q))

    room_messages = Message.objects.all()
    return render(request, 'playground/activity.html', {"topics":topics, "room_messages":room_messages})

# def updateRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     username = room.object.get('username')
#     password = room.object.get('password')
#     if request.method == 'POST':
#         room.username = request.POST.get('username')
#         room.password = request.POST.get('password')
#         form.save()
#         return redirect('home')
#     context = {'form':form}
#     return render(request, 'playground/room_form.html', context)

