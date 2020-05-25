from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Piew, Comment, User, Avatar
from .forms import AvatarForm

def index(request):
    if not request.user.is_authenticated:
        return render(request,"core/login.html", {"message": None})
    context = {
        "user": request.user,
        "piews": Piew.objects.filter().order_by('-created_at')
    }
    return render(request, "core/index.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "core/login.html", {"message": "Invalid credentials."})

def logout_view(request):
      logout(request)
      return render(request, "core/login.html", {"message": "Logged out."})

def register(request):
     # Registration should come through a submission form, POST request.
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        if not password == password_repeat:
            return render(request, "core/register.html", {"message": "Passwords do not match."})
        user = User.objects.create_user(email, username, password)
        user.image = Avatar.objects.get(pk=8)
        user.save()     # Need to save the model, like a DB commit
        return render(request, "core/login.html", {"message": "Successfully registered.  Please log in."})

    else:
        # A GET request means we got to the register page by clicking the link (from the Login page)
        return render(request, "core/register.html")

def piew_view(request):
    user = request.user
    content = request.POST.get("content")
    if len(content) != 0:
        piew = Piew(user=user, content=content)
        if request.FILES:
            image = request.FILES.get("image")
            piew.image = image
        piew.save()

    return HttpResponseRedirect(reverse("index"))

def like(request, id):
    try:
        piew = Piew.objects.get(pk=id)
    except Piew.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    piew.likes.add(request.user.id)
    piew.like_counter += 1

    piew.save()
    return HttpResponseRedirect(reverse("index"))

def comment(request, id):
    try:
        piew = Piew.objects.get(pk=id)
    except Piew.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    if request.POST:
        content = request.POST.get("comment")

        comment = Comment(piew=piew, user=request.user, content=content)

        comment.save()
    
    context = {
        "comments": Comment.objects.all().filter(piew=piew).order_by("-created_at"),
        "piew": piew
    }

    return render(request, "core/comments.html", context)

def user(request, id):
    user = User.objects.get(pk=id)
    context = {
        "piews": Piew.objects.all().filter(user=user).order_by("-created_at"),
        "useR": user,
        "user": request.user,
        "fr": user.followers_counter,
        "fi": user.following_counter,
    }
    return render(request, "core/user.html", context)

def dislike(request, id):
    try:
        piew = Piew.objects.get(pk=id)
    except Piew.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    piew.likes.remove(request.user)
    if piew.like_counter != 0:
        piew.like_counter -= 1

    piew.save()
    return HttpResponseRedirect(reverse("index"))

def delete_piew(request, id):
    try:
        piew = Piew.objects.get(pk=id)
    except Piew.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    if request.user == piew.user:
        piew.delete()
    return HttpResponseRedirect(reverse("index"))

def delete_comment(request, id):
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    if request.user == comment.user: 
        comment.delete()
    return HttpResponseRedirect(reverse("index"))

def likes(request, id):
    piew = Piew.objects.get(pk=id)

    context = {
        "users": piew.likes.all(),
        "piew": piew
    }
    return render(request, "core/likes.html", context)

def follow(request, id):
    user1 = User.objects.get(pk=id)
    user2 = request.user

    user2.following.add(user1)
    user1.followers.add(user2)

    user1.followers_counter += 1
    user2.following_counter += 1

    user1.save()
    user2.save()

    context = {
        "piews": Piew.objects.all().filter(user=user1).order_by("-created_at"),
        "useR": user1,
        "user": user2,
        "fr": user1.followers_counter,
        "fi": user1.following_counter,
    }

    return render(request, "core/user.html", context)

def followers(request, id):
    user = User.objects.get(pk=id)

    context = {
        "users": user.followers.all(),
        "useR": user,
        "user": request.user,
    }
    return render(request, "core/followers.html", context)

def unfollow(request, id):
    user1 = User.objects.get(pk=id)
    user2 = request.user

    user2.following.remove(user1)
    user1.followers.remove(user2)

    if user1.followers_counter != 0:
        user1.followers_counter -= 1
    if user2.following_counter != 0:
        user2.following_counter -= 1

    user1.save()
    user2.save()

    context = {
        "piews": Piew.objects.all().filter(user=user1).order_by("-created_at"),
        "useR": user1,
        "user": user2,
        "fr": user1.followers_counter,
        "fi": user1.following_counter,
    }

    return render(request, "core/user.html", context)

def following(request, id):
    user = User.objects.get(pk=id)

    context = {
        "users": user.following.all(),
        "useR": user,
        "user": request.user,
    }
    return render(request, "core/followers.html", context)

def avatar(request):
    if request.POST:
        user = request.user

        form = AvatarForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
        else:
            print("nao deu otavio")
        context = {
            "piews": Piew.objects.all().filter(user=user).order_by("-created_at"),
            "useR": user,
            "user": user,
            "fr": user.followers_counter,
            "fi": user.following_counter,
        }
        user.image = Avatar.objects.latest('id')
        user.save()
        return render(request, "core/user.html", context)
    else:
        context = {
            "form": AvatarForm()
        }
        return render(request, "core/avatar.html", context)

def search(request):
    username = request.POST.get("ss")
    user = User.objects.filter(username=username)
    if user:
        context = {
            "piews": Piew.objects.all().filter(user=user[0]).order_by("-created_at"),
            "useR": user[0],
            "user": request.user,
            "fr": user[0].followers_counter,
            "fi": user[0].following_counter
        }
        return render(request, "core/user.html", context)
    else:
        context = {
            "user": request.user
        }
        return render(request, "core/404.html", context)
    