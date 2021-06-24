from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "chat/lists.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("lists"))
        else:
            return render(request, "chat/login.html", {
                    "message": "Invalid credentials."
                })
    else:
        return render(request,"chat/login.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
            login(request, user)
            return redirect('lists')
    else:
        form = SignUpForm()
    return render(request, 'chat/signup.html', {'form': form})


@login_required(login_url='login')
def lists(request):
    profile = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(user = profile)
    if request.method == "POST":
        query_name = request.POST.get('user') 
        if query_name:
            results = User.objects.filter(username__icontains=query_name)
            return render(request, 'chat/lists.html', {
                "results":results,
                "profile":profile,
            })

    return render(request, "chat/lists.html",{
        "profile":profile,
    })

@login_required(login_url='login')
def profile(request,username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    request.session['friend_username'] = username
    return render(request, "chat/profile.html",{
        'user': user,
        'profile' : profile,
    })

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def addfriend(request):
    friend_username = request.session.get('friend_username')
    username = request.user.username     
    if not friend_username==username:
        sender = User.objects.get(username = username) 
        receiver = User.objects.get(username = friend_username) 
        receiver = Profile.objects.get(user = receiver) 
    
        receiver.friend_request.add(sender)
    return redirect('lists')

@login_required(login_url='login')
def acceptfriend(request,friend_request):
    username = request.user.username
   
    senderU = User.objects.get(username = friend_request) 
    senderP = Profile.objects.get(user = senderU) 

    receiverU = User.objects.get(username = username)
    receiverP = Profile.objects.get(user = receiverU) 

    senderP.friend_list.add(receiverU)
    receiverP.friend_list.add(senderU)

    receiverP.friend_request.remove(senderU)

    print("fr",friend_request)

    return redirect('lists')

@login_required(login_url='login')
def declinefriend(request,friend_request):
    username = request.user.username
   
    senderU = User.objects.get(username = friend_request) 
    receiverU = User.objects.get(username = username)
    receiverP = Profile.objects.get(user = receiverU) 
    receiverP.friend_request.remove(senderU)

    return redirect('lists')


@login_required(login_url='login')
def message(request,friend_list):
    friendname = User.objects.get(username = friend_list )
    form = MessageForm()
    request.session['friend_list'] = friend_list
    allmessages1 = Message.objects.filter(sender=request.user,receiver=friendname)
    allmessages2 = Message.objects.filter(sender=friendname,receiver=request.user)
    allmessages = allmessages1.union(allmessages2)

    return render(request, 'chat/message.html',{
        'friendname' : friendname,              #'friend_list':friend_list,
        'form' : form,
        'message' : allmessages,

        })

def send(request):
    message = request.POST["text"]
    date = request.POST["date"]
    form = MessageForm()
    friend_list = request.session.get('friend_list')
    friendname = User.objects.get(username = friend_list )
    message_details = Message(text=message,date=date)
    message_details.save()
    message_details.sender.add(request.user)
    message_details.receiver.add(friendname)
    allmessages1 = Message.objects.filter(sender=request.user,receiver=friendname)
    allmessages2 = Message.objects.filter(sender=friendname,receiver=request.user)
    allmessages = allmessages1.union(allmessages2)
    return render(request, 'chat/message.html',{
        
        'message' : allmessages,
        'date': date,
        'friendname' : friendname,
        'form' : form,
    })