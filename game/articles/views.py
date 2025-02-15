from django.shortcuts import render
from .models import Article

# Create your views here.

def articles(request):
    articles = Article.objects.all()
    return render(request, 'articles/articles.html', {'articles': articles})




