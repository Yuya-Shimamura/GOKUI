# import from django
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# モデル、フォーム
from .models import Post
from .forms import PostEditForm

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

class IndexView(ListView):
    model = Post
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

        liked = False
        if post.like.filter(id=request.user.id).exists():
            liked = True

        post.views += 1
        post.save()
        return render(request, 'main_app/post_detail.html', {
            'post': post,
            'liked': liked,
        })
        
def like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    
    liked = False
    if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            liked = False
    else:
        post.like.add(request.user)
        liked = True

    context = {
        'post': post,
        'liked': liked,
    }
    if request.is_ajax():
        html = render_to_string('main_app/like.html', context, request=request)
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