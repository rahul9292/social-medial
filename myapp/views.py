from django.shortcuts import render,redirect, get_object_or_404
from .models import post,Message,Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


# Create your views here.

def home(request):
    formshow = post.objects.all().order_by('-date')
    query = request.GET.get('q')
    users = User.objects.none()

    if query:
        users= User.objects.filter(
            Q(username__icontains=query) 
                
        ).distinct()
    return render (request,'home.html',{'formshow':formshow,'query':query,'users':users})

def posts(request):
    if request.method=="POST":
        
        content = request.POST.get('content')
        image  =request.FILES.get('image')
        form = post(content=content,image=image,author=request.user)
        form.save()
        return redirect('home')
    return render(request,'post.html')

def message(request):
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'message.html', {'all_users': all_users})


def chat(request,username):
    
    other_user = User.objects.get(username=username)
    all_users = User.objects.exclude(id=request.user.id)

    messages = Message.objects.filter(
        sender__in = [request.user,other_user],
        receiver__in = [request.user,other_user]
    ).order_by('time')

    if request.method =="POST":
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            Message.objects.create(
                sender = request.user,
                receiver = other_user,
                content = content,
                image = image
            )
            return redirect('chat',username = other_user.username)


    return render(request,'message.html',{
        'messages': messages,
        'other_user': other_user,
        'all_users': all_users
          })


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = post.objects.filter(author=profile_user).order_by('-date')

    # Make sure Profile exists for this user
    try:
        profile = profile_user.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=profile_user)

    # Handle profile picture upload
    if request.user == profile_user and request.method == 'POST' and 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile', username=username)

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'user_posts': user_posts
    })

