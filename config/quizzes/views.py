from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Quiz, Attempt, Question
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min

def create_quiz(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role != "teacher":
        return redirect("dashboard")
    if request.method == "POST":
        title = request.POST['title']

        quiz = Quiz.objects.create(
            title=title,
            creator=request.user
        )

        return redirect("add_questions", quiz_id=quiz.id)

    return render(request, "create_quiz.html")

def add_questions(request, quiz_id):
    profile = Profile.objects.get(user=request.user)
    if profile.role != "teacher":
        return redirect("dashboard")
    quiz = Quiz.objects.get(id=quiz_id)

    if request.method == "POST":
        text = request.POST['text']
        option_a = request.POST['option_a']
        option_b = request.POST['option_b']
        option_c = request.POST['option_c']
        option_d = request.POST['option_d']
        correct_option = request.POST['correct_option']

        Question.objects.create(
            quiz=quiz,
            text=text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option
        )

    questions = quiz.question_set.all()

    return render(request, "add_questions.html", {
        "quiz": quiz,
        "questions": questions
    })

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == "POST":
        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_option:
                score += 1

        Attempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score
        )

        return redirect("leaderboard", quiz_id=quiz.id)

    return render(request, "take_quiz.html", {
        "quiz": quiz,
        "questions": questions
    })

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role == "teacher":
        quizzes = Quiz.objects.filter(creator=request.user)
        return render(request, "teacher_dashboard.html", {"quizzes": quizzes})
    else:
        quizzes = Quiz.objects.all()
        return render(request, "student_dashboard.html", {"quizzes": quizzes})
    
@login_required
def leaderboard(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = Attempt.objects.filter(quiz=quiz).order_by('-score')

    return render(request, "leaderboard.html", {
        "quiz": quiz,
        "attempts": attempts
    })

@login_required
def quiz_statistics(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.creator != request.user:
        return redirect("dashboard")

    attempts = Attempt.objects.filter(quiz=quiz)

    stats = attempts.aggregate(
        average=Avg('score'),
        highest=Max('score'),
        lowest=Min('score')
    )

    total_attempts = attempts.count()

    return render(request, "quiz_statistics.html", {
        "quiz": quiz,
        "stats": stats,
        "total_attempts": total_attempts
    })

@login_required
def edit_quiz(request, quiz_id):
    profile = Profile.objects.get(user=request.user)
    if profile.role != "teacher":
        return redirect("dashboard")
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.creator != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        quiz.title = request.POST['title']
        quiz.save()
        return redirect("dashboard")

    return render(request, "edit_quiz.html", {"quiz": quiz})

@login_required
def delete_quiz(request, quiz_id):
    profile = Profile.objects.get(user=request.user)
    if profile.role != "teacher":
        return redirect("dashboard")
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.creator != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        quiz.delete()
        return redirect("dashboard")

    return render(request, "delete_quiz.html", {"quiz": quiz})