from django.contrib import auth, messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.contenttypes.models import ContentType
from askme_app.models import Question, Tag, Answer, Vote
from askme_app.forms import LoginForm, SignupForm, NewQuestionForm, NewAnswerForm, SettingsForm


@require_http_methods('GET')
def index(request):
    page_obj = paginate(Question.objects.sorted_by_created_at(), request)

    context = {'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
               }

    return render(request, 'index.html', context)


@csrf_protect
@require_http_methods(['GET', 'POST'])
def show_question(request, question_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        answer_form = NewAnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(request.user, question_id)
            answer_index = list(Answer.objects.sorted_by_rating(question_id)).index(answer)
            page_number = answer_index // 3 + 1
            return redirect(reverse('question', args=[question_id]) + f"?page={page_number}")
    else:
        answer_form = NewAnswerForm()

    page_obj = paginate(Answer.objects.sorted_by_rating(question_id), request, 3)

    context = {
        'question': Question.objects.get(pk=question_id),
        'global_tags': Tag.objects.sort_by_related_question_quantity()[:10],
        'page_obj': page_obj,
        'form': answer_form,
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
    cont = request.GET.get('continue')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request=request, **login_form.cleaned_data)

            login(request, user)
            cont = request.POST.get("continue", None)
            return redirect(cont if cont and cont != "None" else reverse('index'))

        else:
            username_value = request.POST.get('username')
            login_form = LoginForm(request.POST, initial={'username': username_value})
            return render(request, 'login.html', {'form': login_form})
    else:
        login_form = LoginForm()

    return render(request, 'login.html', context={'form': login_form, 'continue': cont})


@csrf_protect
@require_http_methods(['GET', 'POST'])
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user, profile = form.save()

            authenticated_user = authenticate(request=request,
                                              username=user.username,
                                              password=form.cleaned_data['password'])
            login(request, authenticated_user)
            return redirect('index')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@csrf_protect
@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def new_question(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request.user)
            return redirect('question', question_id=question.id)
    else:
        form = NewQuestionForm()

    context = {'form': form, 'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]}
    return render(request, 'new_question.html', context)


@require_http_methods(['GET'])
def show_by_tag(request, title):
    page_obj = paginate(Question.objects.filter_by_tag(title), request)

    context = {'tag': Tag.objects.get(title=title),
               'page_obj': page_obj,
               'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]
               }
    return render(request, 'show_tag.html', context)


@csrf_protect
@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['POST'])
def log_out(request):
    auth.logout(request)
    return redirect(reverse('index'))


@csrf_protect
@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['POST'])
def vote(request):
    print(f"---------------------------{request.POST}")

    content_type = request.POST.get('content_type')
    object_id = int(request.POST.get('object_id'))
    vote_action = request.POST.get('vote_action')
    user = request.user

    if content_type == 'question':
        content_object = get_object_or_404(Question, id=object_id)
    elif content_type == 'answer':
        content_object = get_object_or_404(Answer, id=object_id)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid content type'})

    vote_value = 1 if vote_action == 'upvote' else -1

    vote, created = Vote.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(content_object),
        object_id=object_id,
        author=user,
    )

    if not created:
        if vote.rate == vote_value:
            vote.delete()
        else:
            vote.rate = vote_value
            vote.save()
    else:
        vote.rate = vote_value
        vote.save()

    rating = content_object.get_rating()

    return JsonResponse({'success': True, 'rating': rating})


@csrf_protect
@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    user = request.user

    if request.method == 'POST':
        form = SettingsForm(user, request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            data = {
                'username': u.username,
                'password': u.password
            }
            login_form = LoginForm(data)
            login_form.is_valid()

            authenticated_user = authenticate(request=request, **login_form.cleaned_data)
            login(request, authenticated_user)
            messages.success(request, 'Your account successfully updated')
            return redirect(reverse('settings'))
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
        }
        form = SettingsForm(user, initial=initial_data)

    context = {
        'form': form,
        'global_tags': Tag.objects.sort_by_related_question_quantity()[:10]
    }

    return render(request, 'settings.html', context)


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get('page', 1)

    return paginator.get_page(page_number)
