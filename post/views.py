from django.shortcuts import redirect, render, get_object_or_404

from .models import Post

from .forms import PostForm


# Create your views here.
def index(request):
    posts = Post.objects.all()
    return render(request, 'post/index.html', {'posts': posts})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.author = request.user
            # user.save()
            form.save()
            return redirect('post:index')
    else:
        form = PostForm()
        return render(request, 'post/create_post.html', context={"form": form})


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