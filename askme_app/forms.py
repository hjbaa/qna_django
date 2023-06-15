import os
import profile

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Profile, Tag, Question, Answer


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Username',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password',
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            profile = Profile.objects.get_profile_by_username(username)
            if not profile or not profile.user.check_password(password):
                self.add_error(None, 'Wrong username or password')

        return self.cleaned_data


class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Username'
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Repeat password'
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Avatar'
    )

    def clean_username(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if Profile.objects.get_profile_by_username(username):
            self.add_error('username', IntegrityError("Profile with this username already exists"))
        return username

    def clean_email(self):
        super().clean()
        email = self.cleaned_data.get('email')
        if Profile.objects.get_profile_by_email(email):
            self.add_error('email', IntegrityError("Profile with this email already exists"))
        return email

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("repeat_password")
        if password and password != repeat_password:
            self.add_error('repeat_password', ValidationError("Passwords don't match", code='invalid'))
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)

        # Создание профиля
        avatar = self.files.get('avatar')
        profile = Profile.objects.create(user=user, avatar=avatar)

        return user, profile


class SettingsForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.label_suffix = ""

    username = forms.CharField(
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Username'
    )

    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )

    old_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "Leave blank if you don't change your password"
        }),
        label='Old password'
    )

    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New password'
    )

    new_repeat_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Repeat password'
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Avatar'
    )

    def clean_username(self):
        return self.user.username

    def clean_old_password(self):
        return self.cleaned_data.get('new_repeat_password')

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']

        if old_password and not self.user.check_password(old_password):
            self.add_error('old_password', ValidationError("Your old password is incorrect", code='invalid'))

        return old_password

    def clean_email(self):
        super().clean()
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=self.user.username).exists():
            self.add_error('email', ValidationError("Email address is already in use", code='invalid'))

        return email

    def clean(self):
        super().clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        new_repeat_password = self.cleaned_data.get('new_repeat_password')

        if new_password and not old_password:
            self.add_error('new_password', ValidationError("You must enter your old password", code='invalid'))

        if new_password and not new_repeat_password:
            self.add_error('new_repeat_password', ValidationError("You must repeat new password", code='invalid'))
            return self.cleaned_data

        if new_password and new_password != new_repeat_password:
            self.add_error('new_repeat_password', ValidationError("New passwords don't match", code='invalid'))

        return self.cleaned_data

    def save(self):
        email = self.cleaned_data['email']
        new_password = self.cleaned_data['new_password']
        avatar = self.files.get('avatar')

        if email:
            self.user.email = email

        if new_password:
            self.user.set_password(new_password)

        if avatar:
            self.user.profile.avatar = avatar

        self.user.save()
        self.user.profile.save()
        return self.user


class NewQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Title'
    )

    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Body'
    )

    tags = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tags separated by commas'}),
        label='Tags'
    )

    def save(self, user):
        super().clean()
        question = Question.objects.create(
            title=self.cleaned_data['title'],
            body=self.cleaned_data['body'],
            author=user
        )
        tags = self.cleaned_data.get('tags')
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(title=tag_name)
            question.tags.add(tag)
        return question


class NewAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control mb-4', 'placeholder': 'Type your answer here'})
    )

    def save(self, user, question_id):
        body = self.cleaned_data['body']
        question = Question.objects.get(pk=question_id)

        answer = Answer(body=body, question=question, author=user)
        answer.save()

        return answer
