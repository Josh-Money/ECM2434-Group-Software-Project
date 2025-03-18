from django.urls import path
from . import views

urlpatterns = [
    path("", views.articles, name="articles"),
    path("<int:article_id>/", views.articles, name="article_detail"),  # Redirect to articles view
    path("question/<int:question_id>/", views.get_question_answer, name="get_question_answer"),
]