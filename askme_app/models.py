from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from askme_django.settings import MEDIA_URL
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Vote(models.Model):
    rate = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return f"rate:{self.rate};\tcontent_type:{self.content_type};\tauthor:{self.author_id}"

    class Meta:
        unique_together = ('author', 'content_type', 'object_id',)


class TagManager(models.Manager):
    def sort_by_related_question_quantity(self):
        return self.annotate(num_questions=Count('question')).order_by('-num_questions')


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TagManager()

    def __str__(self):
        return f"id: {self.id};\t title: {self.title}"


class QuestionManager(models.Manager):
    def sorted_by_rating(self):
        return self.annotate(total_votes=Sum('votes__rate')).order_by('-total_votes')

    def sorted_by_created_at(self):
        return self.order_by('-created_at')

    def filter_by_tag(self, tag_title):
        return self.filter(tags__title=tag_title)


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    votes = GenericRelation(Vote)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    objects = QuestionManager()

    def __str__(self):
        return f"title: {self.title};\t votes: {self.votes};"

    def get_rating(self):
        rating = self.votes.aggregate(Sum('rate'))['rate__sum']
        return rating if rating is not None else 0

    def answers_count(self):
        return Count(Answer.objects.filter(question_id=self.id))


class Answer(models.Model):
    body = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = GenericRelation(Vote)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return f"question_id: {self.question_id};\t votes: {self.votes}"

    def get_rating(self):
        rating = self.votes.aggregate(Sum('rate'))['rate__sum']
        return rating if rating is not None else 0


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=MEDIA_URL)
    created_at = models.DateTimeField(auto_now_add=True)
    # author
