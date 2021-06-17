from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post  # .models because from same folder
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView)


# function based view
# def home(request):
#     context = {
#         "posts": Post.objects.all()
#     }
#     return render(request, "blog/home.html", context)


# Home page
# class based view
class PostListView(ListView):
    # tells view which model to query to make list
    model = Post
    # <app>/<model>_<view_type>.html is expected pattern for templates
    # in this case: blog/post_list.html
    # we want to use our own, so defined below
    template_name = 'blog/home.html'
    # use variable name 'posts' instead of 'objectlist' to pass to template
    context_object_name = 'posts'
    # order posts from oldest to newest
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        # get username from url
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# this view uses the expected names from django
class PostDetailView(DetailView):
    model = Post


# LoginRequiredMixin ensures there is a logged in user for creation
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # override normal form_valid so we can set current user as author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # function used by UserPassesTestMixin
    def test_func(self):
        # get current post object we are trying to update
        post = self.get_object()
        # ensure current user is author of post
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # tell the site where to send user upon successful deletion
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
