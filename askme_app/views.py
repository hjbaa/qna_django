from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from askme_app.models import Question, Tag, Answer
from askme_app.forms import LoginForm


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


@csrf_protect
def log_in(request):
    login_form = None

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request=request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = 'Wrong username or password!'
                login_form = LoginForm()
                return render(request, 'login.html', {'error_message': error_message, 'form': login_form})
    elif request.method == 'GET':
        login_form = LoginForm()

    return render(request, 'login.html', context={'form': login_form})



    # if request.method == 'POST':
    #     if not request.POST.get('csrfmiddlewaretoken'):
    #         error_message = 'Ошибка валидации формы. Попробуйте еще раз.'
    #         return render(request, 'login.html', {'error_message': error_message})
    #
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #
    #     user = authenticate(request, email=email, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('index')
    #     else:
    #         error_message = 'Wrong username or password!'
    #         return render(request, 'login.html', {'error_message': error_message})
    # else:
    #     return render(request, 'login.html')


@csrf_protect
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
