from django.urls import path
from .views import profile_view

urlpatterns = [
    # When users navigate to '/profile/' (as included in the project's urls),
    # this view will be rendered.
    path('', profile_view, name='profile'),
]
