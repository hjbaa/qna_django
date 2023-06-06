from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from askme_app.models import Question, Tag, Answer


# Create your views here.

def index(request):
    page_obj = paginate(Question.objects.sorted_by_created_at(), request)

    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'index.html', context)


def show_question(request, question_id):
    page_obj = paginate(Answer.objects.filter(question_id=question_id), request, 3)

    context = {'question': Question.objects.get(pk=question_id),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               'page_obj': page_obj,
               }
    return render(request, 'show_question.html', context)


def hot(request):
    page_obj = paginate(Question.objects.sorted_by_rating(), request)
    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'hot.html', context)


def log_in(request):
    if request.method == 'POST':
        if not request.POST.get('csrfmiddlewaretoken'):
            error_message = 'Ошибка валидации формы. Попробуйте еще раз.'
            return render(request, 'login.html', {'error_message': error_message})

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Wrong username or password!'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def sign_up(request):
    return render(request, 'signup.html')


def new_question(request):
    context = {'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]}

    return render(request, 'new_question.html', context)


def show_by_tag(request, title):
    page_obj = paginate(Question.objects.filter_by_tag(title), request)

    context = {'tag': Tag.objects.get(title=title),
               'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]
               }
    return render(request, 'show_tag.html', context)


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)

    return paginator.get_page(page_number)
