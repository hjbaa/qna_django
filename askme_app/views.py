from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from askme_app.models import Question, Tag, Answer
from askme_app.forms import LoginForm


@require_http_methods('GET')
def index(request):
    page_obj = paginate(Question.objects.sorted_by_created_at(), request)

    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'index.html', context)


@require_http_methods(['GET'])
def show_question(request, question_id):
    page_obj = paginate(Answer.objects.filter(question_id=question_id), request, 3)

    context = {'question': Question.objects.get(pk=question_id),
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               'page_obj': page_obj,
               }
    return render(request, 'show_question.html', context)


@require_http_methods(['GET'])
def hot(request):
    page_obj = paginate(Question.objects.sorted_by_rating(), request)
    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'hot.html', context)


@csrf_protect
@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request=request, **login_form.cleaned_data)

            login(request, user)
            return redirect(reverse('index'))

        else:
            username_value = request.POST.get('username')
            login_form = LoginForm(request.POST, initial={'username': username_value})
            return render(request, 'login.html', {'form': login_form})
    else:
        login_form = LoginForm()

    return render(request, 'login.html', context={'form': login_form})


@csrf_protect
@require_http_methods(['GET', 'POST'])
def sign_up(request):
    return render(request, 'signup.html')


@require_http_methods(['GET', 'POST'])
def new_question(request):
    context = {'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]}

    return render(request, 'new_question.html', context)


@require_http_methods(['GET'])
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
