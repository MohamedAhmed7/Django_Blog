from django.shortcuts import render

# Create your views here.
posts = [
    {
        'title':'first post',
        'author':'Mohamed',
        'date': '2021-1-17',
        'content': 'first blog post'
    },
{
        'title':'first post',
        'author':'Ahmed',
        'date': '2021-1-17',
        'content': 'Second blog post'
    }

]
def home(request):
    context = {
        'title':'home',
        'posts':posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')
