from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import PostForm, CommentForm

@login_required
def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    search = request.GET.get('search', '')
    if search:
        post_list = post_list.filter(title__icontains=search) | post_list.filter(content__icontains=search)
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'search': search})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})
from django.http import HttpResponseForbidden

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Verify user is the author
    if request.user != post.author:
        return HttpResponseForbidden("You don't have permission to delete this post")
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return redirect('post_detail', post_id=post.id)
@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    
    if request.user != comment.author:
        return HttpResponseForbidden("You can't edit this comment")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'post_id': post_id,
        'comment': comment
    })

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    
    if request.user != comment.author:
        return HttpResponseForbidden("You can't delete this comment")
    
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=post_id)
    
    return render(request, 'blog/confirm_delete_comment.html', {
        'comment': comment,
        'post_id': post_id
    })