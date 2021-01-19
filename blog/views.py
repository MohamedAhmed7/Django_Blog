from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Reply
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

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(post = context['post']).all()
        return context

def about(request):
    return render(request, 'blog/about.html')
