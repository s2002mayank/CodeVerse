from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Channel, Topic, Message, User
from .forms import ChannelForm, UserForm, MyUserCreationForm

# Create your views here.

# channels = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    channels = Channel.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    channel_count = channels.count()
    channel_messages = Message.objects.filter(
        Q(channel__topic__name__icontains=q))[0:3]

    context = {'channels': channels, 'topics': topics,
               'channel_count': channel_count, 'channel_messages': channel_messages}
    return render(request, 'base/home.html', context)


def channel(request, pk):
    channel = Channel.objects.get(id=pk)
    channel_messages = channel.message_set.all()
    participants = channel.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            channel=channel,
            body=request.POST.get('body')
        )
        channel.participants.add(request.user)
        return redirect('channel', pk=channel.id)

    context = {'channel': channel, 'channel_messages': channel_messages,
               'participants': participants}
    return render(request, 'base/channel.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    channels = user.channel_set.all()
    channel_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'channels': channels,
               'channel_messages': channel_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createChannel(request):
    form = ChannelForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Channel.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/channel_form.html', context)


@login_required(login_url='login')
def updateChannel(request, pk):
    channel = Channel.objects.get(id=pk)
    form = ChannelForm(instance=channel)
    topics = Topic.objects.all()
    if request.user != channel.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        channel.name = request.POST.get('name')
        channel.topic = topic
        channel.description = request.POST.get('description')
        channel.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'channel': channel}
    return render(request, 'base/channel_form.html', context)


@login_required(login_url='login')
def deleteChannel(request, pk):
    channel = Channel.objects.get(id=pk)

    if request.user != channel.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        channel.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': channel})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    channel_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'channel_messages': channel_messages})