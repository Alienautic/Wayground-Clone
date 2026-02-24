from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create-quiz/", views.create_quiz, name="create_quiz"),
    path("add-questions/<int:quiz_id>/", views.add_questions, name="add_questions"),
    path("take/<int:quiz_id>/", views.take_quiz, name="take_quiz"),
    path("leaderboard/<int:quiz_id>/", views.leaderboard, name="leaderboard"),
    path("statistics/<int:quiz_id>/", views.quiz_statistics, name="quiz_statistics"),
    path("edit/<int:quiz_id>/", views.edit_quiz, name="edit_quiz"),
    path("delete/<int:quiz_id>/", views.delete_quiz, name="delete_quiz"),
]