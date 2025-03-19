from django.urls import path
from .views import profile_view, update_profile_picture

urlpatterns = [
    # When users navigate to '/profile/' (as included in the project's urls),
    # this view will be rendered.
    path('', profile_view, name='profile'),
    path('update-picture/', update_profile_picture, name='update_profile_picture'),
    path('<str:username>/', profile_view, name='profile_detail'),
]
