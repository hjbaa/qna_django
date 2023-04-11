from django.http import HttpResponse
from django.shortcuts import render

from askme_app.models import Question, Tag, Answer


# Create your views here.

def index(request):
    context = {'questions': Question.objects.sorted_by_created_at(),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'index.html', context)


def show_question(request, question_id):
    context = {'question': Question.objects.get(pk=question_id),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               'answers': Answer.objects.filter(question_id=question_id)
               }
    return render(request, 'show_question.html', context)


def hot(request):
    context = {'questions': Question.objects.sorted_by_rating(),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

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
