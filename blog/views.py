from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView,
CreateView, UpdateView, DeleteView)
from django.contrib import messages
from .models import Post, Reply
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.forms import HiddenInput

# Create your views here.

def home(request):
    context = {
        'title':'home',
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # order from newest to oldest
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    # override the base query function to list posts for specific user
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        context['profile'] = user
        return context
'''
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    # pass the replies to the post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(post = context['post']).all()

        return context
'''
class addReply(forms.ModelForm):
    reply = forms.Textarea()
    class Meta:
        model = Reply
        fields = ['reply', 'author', 'post']
        widgets = {'author': forms.HiddenInput(), 'post':forms.HiddenInput(),
                   'reply': forms.Textarea(attrs={'rows':3})
                   }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(addReply, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['author'].required = False
        self.fields['post'].required = False

    def save(self, commit=True):
        user = self.fields['author']
        post = self.fields['post']
        content = self.cleaned_data.get('reply')
        rep = Reply(reply = content, post = post, author = user)
        rep.save()



def detailPost(request, pk):
    post = Post.objects.filter(id = pk).first()
    form = addReply(request.POST)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Login First to add replies to posts')
            return redirect('login')
        elif form.is_valid() :
            form.fields['author'] = request.user
            form.fields['post'] = post
            form.save()
            messages.success(request, 'Your Replied to this post')
            return redirect('post-detail', pk=post.id)

    context = {
        'title':'home',
        'post': post ,
        'replies': Reply.objects.filter(post = post).all(),
        'form': addReply,
    }

    return render(request, 'blog/post_detail.html', context)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html')
