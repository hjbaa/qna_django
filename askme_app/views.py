from django.http import HttpResponse
from django.shortcuts import render

from askme_app.models import Question


# Create your views here.

def index(request):
    questions = Question.objects.all()
    context = {'questions': questions}

    return render(request, 'index.html', context)


def show_question(request, question_id):
    return render(request, 'show_question.html')


def hot(request):
    return render(request, 'hot.html')


def log_in(request):
    return render(request, 'login.html')


def sign_up(request):
    return render(request, 'signup.html')


def new_question(request):
    return render(request, 'new_question.html')


def show_by_tag(request):
    return render(request, 'show_tag.html')
