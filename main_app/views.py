from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post
from .forms import PostEditForm

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

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = "main_app/post_detail.html"

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