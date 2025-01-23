from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *


# home
def index(request):
    posts = Post.objects.filter(user_id=request.user.id).order_by("id").reverse()
    top_posts = Post.objects.all().order_by("-likes")
    recent_posts = Post.objects.all().order_by("-id")
    categories = Post.objects.values_list('category', flat=True).distinct()
    return render(request, "index.html", {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'user': request.user,
        'media_url': settings.MEDIA_URL
    })


# 登録
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username, email=email, password=password).save()
                return redirect('signin')
        else:
            messages.info(request, "Password should match")
            return redirect('signup')

    return render(request, "signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, 'Username or Password is incorrect')
            return redirect("signin")

    return render(request, "signin.html")


def logout(request):
    auth.logout(request)
    return redirect('index')


# 記事を展示する
def blog(request, author_username=None):
    if author_username:
        author = get_object_or_404(User, username=author_username)
        posts = Post.objects.filter(user=author).order_by("id").reverse()
    else:
        posts = Post.objects.all().order_by("id").reverse()

    top_posts = Post.objects.all().order_by("-likes")
    recent_posts = Post.objects.all().order_by("-id")

    return render(request, "blog.html", {
        'posts': posts,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'user': request.user,
        'media_url': settings.MEDIA_URL,
        'author': author if author_username else None
    })


def create(request):
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES['image']
            Post(postname=postname, content=content, category=category, image=image, user=request.user).save()
        except:
            print("Error")
        return redirect('index')
    else:
        return render(request, "create.html")


def profile(request, id):
    profile_user = User.objects.get(id=id)
    return render(request, 'profile.html', {
        'profile': profile_user,
        'posts': Post.objects.filter(user_id=profile_user.id),
        'media_url': settings.MEDIA_URL,
        'user': request.user,  # Pass the currently logged-in user
    })


def profileedit(request, id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        image = request.FILES.get('image')

        user = User.objects.get(id=id)
        user.first_name = firstname
        user.email = email
        user.last_name = lastname
        user.save()
        return profile(request, id)
    return render(request, "profileedit.html", {
        'user': User.objects.get(id=id),
    })


@login_required
def increaselikes(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.likes += 1
        post.save()
    return redirect("index")


def post(request, id):
    post = Post.objects.get(id=id)

    return render(request, "post-details.html", {
        "user": request.user,
        'post': Post.objects.get(id=id),
        'recent_posts': Post.objects.all().order_by("-id"),
        'media_url': settings.MEDIA_URL,
        'comments': Comment.objects.filter(post_id=post.id),
        'total_comments': len(Comment.objects.filter(post_id=post.id))
    })


def savecomment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id=post.id, user_id=request.user.id, content=content).save()
        return redirect('post', id=post.id)


def deletecomment(request, id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()
    return post(request, postid)


def editpost(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']

            post.postname = postname
            post.content = content
            post.category = category
            post.save()
        except:
            print("Error")
        return profile(request, request.user.id)

    return render(request, "postedit.html", {
        'post': post
    })


@login_required
def deletepost(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'confirm_delete.html', {'post': post})


@login_required
def follow(request, id):
    user_to_follow = User.objects.get(id=id)
    user_profile = User.objects.get(user=request.user)
    user_profile.following.add(user_to_follow)
    return redirect('index')


@login_required
def unfollow(request, id):
    user_to_unfollow = User.objects.get(id=id)
    user_profile = User.objects.get(user=request.user)
    user_profile.following.remove(user_to_unfollow)
    return redirect('index')

# def contact_us(request):
#     context = {}
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#
#         obj = Contact(name=name, email=email, subject=subject, message=message)
#         obj.save()
#         context['message'] = f"Dear {name}, Thanks for your time!"
#
#     return render(request, "contact.html")
