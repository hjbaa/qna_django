import os
import profile

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Profile, Tag, Question


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
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your answer here'})
    )

    def save(self):
        ...
