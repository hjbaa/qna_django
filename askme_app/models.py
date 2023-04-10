from django.db import models
from django.contrib.auth.models import User
from askme_django.settings import MEDIA_URL
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Vote(models.Model):
    rate = models.IntegerField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    votes = GenericRelation(Vote)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    body = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = GenericRelation(Vote)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    title = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=MEDIA_URL)
    created_at = models.DateTimeField(auto_now_add=True)

