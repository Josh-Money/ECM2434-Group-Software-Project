# Author: Will Cooke

from django.shortcuts import render

from django.shortcuts import render, redirect

def home(request):
    print('User:', request.user)
    print('Username:', request.user.username)
    print('Is Authenticated:', request.user.is_authenticated)

    if not request.user.is_authenticated:
        return redirect('/')

    context = {
        'page_title': 'Home',
        'welcome_message': 'Welcome to the Home!',
        'description': 'Check out the latest posts and updates here.', 
        'user': {
            'name': request.user.username,
            'points': 100
        }
    }
    return render(request, 'home/home.html', context)


#def post_detail(request, id):
#    return render(request, 'home/post_detail.html', {'post_id': id})