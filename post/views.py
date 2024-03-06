from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import csrf
from django.template.loader import render_to_string

from .models import Post, UserProfile

from .forms import PostForm, SignupForm, ProfileForm, UserForm


# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'post/index.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.save()
            return redirect('post:index')
    else:
        form = PostForm()
        return render(request, 'post/create_post.html', context={"form": form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('post:index')


def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/detail.html', {"post": post})


def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:detail_post', post_id=post.id)
    else:
        form = PostForm(instance=post)
        return render(request, 'post/create_post.html', {'form': form})


def login_to(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('post:index')
        else:
            return render(request, 'post/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'post/login.html')


def logout_from(request):
    try:
        logout(request)
        return redirect('post:index')
    except Exception as e:
        return HttpResponse("An error occurred: " + str(e))


def sign_up_to(request):
    if request.method == "POST":
        user = SignupForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('post:login')
        else:
            return render(request, 'post/sign_up.html', {'form': user})
    else:
        form = SignupForm()
        return render(request, 'post/sign_up.html', {'form': form})


def profile(request):
    user = request.user

    return render(request, 'post/profile.html', {'user': user})


def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            print("Form is valid")
            return redirect('post:profile')

    else:
        form = ProfileForm(instance=user_profile)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {'form': form}
            context.update(csrf(request))

            form_html = render_to_string('post/edit_profile.html', context)
            return JsonResponse({'form': form_html})
        return render(request, 'post/edit_profile.html', {'form': form})


def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('post:profile')
    else:
        form = UserForm(instance=user)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = {'form': form}
            context.update(csrf(request))

            form_html = render_to_string('post/edit_user.html', context)
            return JsonResponse({'form': form_html})
        return render(request, 'post/edit_user.html', {'form': form})


def your_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    return render(request, 'post/your_post.html', {'posts': posts})
