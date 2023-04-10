from django.http import HttpResponse
from django.shortcuts import render

from askme_app.models import Question


# Create your views here.

def index(request):
    questions = Question.objects.all()
    print(questions)

    context = {'questions': 123}

    return render(request, 'index.html', context)


def show_question(request, question_id):
    return render(request, 'question.html')


def log_in(request):
    return render(request, 'login.html')


def sign_up(request):
    return render(request, 'signup.html')


def new_question(request):
    return render(request, 'new_question.html')


def show_by_tag(request):
    return render(request, 'show_tag.html')

