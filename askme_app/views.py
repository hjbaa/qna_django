from django.http import HttpResponse
from django.shortcuts import render

from askme_app.models import Question, Tag


# Create your views here.

def index(request):
    questions = Question.objects.sorted_by_created_at()
    context = {'questions': questions}

    return render(request, 'index.html', context)


def show_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    context = {'question': question}
    return render(request, 'show_question.html')


def hot(request):
    questions = Question.objects.sorted_by_rating()
    context = {'questions': questions}
    return render(request, 'hot.html', context)


def log_in(request):
    return render(request, 'login.html')


def sign_up(request):
    return render(request, 'signup.html')


def new_question(request):
    return render(request, 'new_question.html')


def show_by_tag(request, title):
    tag = Tag.objects.get(title=title)
    return render(request, 'show_tag.html')
