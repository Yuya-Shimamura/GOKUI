# import from django
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count

import datetime

# モデル、フォーム
from .models import Post, Comment
from .forms import PostEditForm, CommentForm

# 検索機能
from django.db.models import Q
from functools import reduce
from operator import and_

# いいね機能
from django.template.loader import render_to_string
from django.http import JsonResponse



class OnlyYourPostMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        return user.pk == post.user.pk or user.is_superuser

class OnlyYourCommentMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        comment = Comment.objects.get(id=self.kwargs['pk'])
        return user.pk == comment.author.pk or user.is_superuser

class IndexView(ListView):
    queryset = Post.objects.order_by('-created_at')
    template_name = "main_app/index.html"
    context_object_name = 'posts'
    paginated_by = 24

class ViewsIndexView(ListView, LoginRequiredMixin):
    queryset = Post.objects.order_by('-views')
    template_name = "main_app/index.html"
    context_object_name = 'posts'
    paginated_by = 24

class LikeIndexView(ListView, LoginRequiredMixin):
    queryset = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')
    template_name = "main_app/index.html"
    context_object_name = 'posts'
    paginated_by = 24

class FavoriteIndexView(ListView, LoginRequiredMixin):
    queryset = Post.objects.annotate(favorite_count=Count('favorite')).order_by('-favorite_count')
    template_name = "main_app/index.html"
    context_object_name = 'posts'
    paginated_by = 24

class OneWeekAgoIndexView(ListView, LoginRequiredMixin):
    start_date = datetime.date.today() - datetime.timedelta(days=7)
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    queryset = Post.objects.filter(created_at__range=(start_date, end_date))
    template_name = "main_app/index.html"
    context_object_name = 'posts'
    paginated_by = 24

class OneMonthAgoIndexView(ListView, LoginRequiredMixin):
    start_date = datetime.date.today() - datetime.timedelta(days=30)
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    queryset = Post.objects.filter(created_at__range=(start_date, end_date))
    template_name = "main_app/index.html"
    context_object_name = 'posts'
    paginated_by = 24

class PostSearchView(TemplateView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.order_by('-id')
        
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', '　'])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            query = reduce(and_, [Q(title__icontains=q) | Q(tags__name__icontains=q) for q in query_list])
            posts = posts.filter(query)

        return render(request, 'main_app/index.html', {
            'keyword': keyword,
            'posts': posts,
        })

class PostTagListView(TemplateView):
    def get(self, request, *args, **kwargs):
        tag = self.kwargs['tag']
        posts = Post.objects.order_by('-id').filter(tags__name__icontains=tag)
        return render(request, 'main_app/index.html', {
            'posts': posts,
            'tag': tag,
        })

class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        favorite_count = request.user.favorite.all().count()
        favorite_rest = 3 - favorite_count

        comment_list = Comment.objects.filter(parent__isnull=True, post=post)

        liked = False
        if post.like.filter(id=request.user.id).exists():
            liked = True

        favored = False
        if post.favorite.filter(id=request.user.id).exists():
            favored = True

        post.views += 1
        post.save()
        return render(request, 'main_app/post_detail.html', {
            'post': post,
            'liked': liked,
            'favored': favored,
            'favorite_rest': favorite_rest,
            'comment_list': comment_list,
        })

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.author = current_user
        comment.save()
        return redirect('post_detail', pk=pk)

    return render(request, 'main_app/comment_form.html', {
        'form': form,
        'post': post,
    })

@login_required
def reply_create(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    current_user = request.user
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.author = current_user
        reply.save()
        return redirect('post_detail', pk=post.id)

    return render(request, 'main_app/comment_form.html', {
        'form': form,
        'post': post,
        'comment': comment,
    })

class CommentDeleteView(DeleteView, LoginRequiredMixin, OnlyYourCommentMixin):
    model = Comment
    template_name = "main_app/comment_delete.html"
    def get_success_url(self):
        post = self.object.post 
        return reverse_lazy('post_detail', kwargs={'pk': post.id})

@login_required
def like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    
    liked = False
    if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            liked = False
    else:
        post.like.add(request.user)
        liked = True
    
    favored = False
    if post.favorite.filter(id=request.user.id).exists():
        favored = True

    context = {
        'post': post,
        'liked': liked,
        'favored': favored,
    }
    if request.is_ajax():
        html = render_to_string('main_app/like.html', context, request=request)
        return JsonResponse({'form': html})

@login_required
def favorite(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    favorite_count = request.user.favorite.all().count()
    favorite_rest = 3 - favorite_count

    favored = False
    if post.favorite.filter(id=request.user.id).exists():
        favorite_rest += 1
        post.favorite.remove(request.user)
        favored = False
    elif request.user not in post.favorite.all() and favorite_rest != 0:
        favorite_rest -= 1
        post.favorite.add(request.user)
        favored = True
    elif favorite_rest == 0:
        pass
    
    liked = False
    if post.like.filter(id=request.user.id).exists():
        liked = True

    context = {
        'post': post,
        'liked': liked,
        'favored': favored,
        'favorite_rest': favorite_rest,
    }
    if request.is_ajax():
        html = render_to_string('main_app/favorite.html', context, request=request)
        return JsonResponse({'form': html})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostEditForm
    template_name = "main_app/post_create.html"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
        

class PostEditView(LoginRequiredMixin, OnlyYourPostMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = "main_app/post_edit.html"
    
    def get_success_url(self):
        postid = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': postid})

class PostDeleteView(LoginRequiredMixin, OnlyYourPostMixin, DeleteView):
    model = Post
    template_name = "main_app/post_delete.html"

    def get_success_url(self):
        user = self.request.user
        userid = user.pk
        return reverse_lazy('profile', kwargs={'pk': userid})


class UserPostListView(ListView):
    def get_queryset(self):
        userid = self.kwargs['pk']
        return Post.objects.filter(user=userid)
    
    context_object_name = 'posts'
    template_name = "main_app/user_post_list.html"