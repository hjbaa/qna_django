import random

import mimesis.types
from django.core.management.base import BaseCommand
from mimesis import Person
from mimesis.locales import Locale
from django.utils import timezone
from askme_app.models import Question, Tag, Vote, Answer, Profile
from django.contrib.auth.models import User
from mimesis import Datetime
from mimesis.random import Random
from mimesis import Text
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Fill database with randomized content'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Indicates the number of rows to be created')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        # 5+ часа кайфа при ratio=10_000
        _fill_users(ratio)
        _fill_tags(ratio)
        _fill_questions(ratio * 10)
        _fill_answers(ratio * 100)
        _fill_votes(ratio * 500)


def _fill_users(ratio):
    for i in range(ratio):
        person = Person(Locale.EN)

        try:
            u = User(first_name=person.first_name(),
                     last_name=person.last_name(),
                     email=person.email(),
                     password=person.password(),
                     is_staff=False,
                     username=person.username(),
                     )

            u.save()
        except IntegrityError:
            continue


def _fill_tags(ratio):
    for i in range(ratio):
        txt = Text(Locale.EN)
        try:
            t = Tag(title=txt.word())
            t.save()
        except IntegrityError:
            continue


def _fill_questions(ratio):
    for i in range(ratio):
        txt = Text(Locale.EN)
        random_user = User.objects.order_by('?').first()

        q = Question(title=txt.quote(),
                     body=txt.text(30),
                     author=random_user
                     )

        q.save()

        tags = Tag.objects.order_by('?')[:5]
        q.tags.set(tags)
        q.save()


def _fill_answers(ratio):
    for i in range(ratio):
        txt = Text(Locale.EN)
        random_user = None
        random_question = None

        while random_user is None:
            try:
                random_user = User.objects.get(pk=random.randint(1, 10000))
            except User.DoesNotExist:
                continue

        while random_question is None:
            try:
                random_question = Question.objects.get(pk=random.randint(1, 100000))
            except User.DoesNotExist:
                continue

        a = Answer(body=txt.text(30), author=random_user, question=random_question, is_correct=False)
        a.save()


def _fill_votes(ratio):
    for i in range(ratio):
        random_model_instance = None

        if random.randint(0, 1) == 0:
            while random_model_instance is None:
                try:
                    random_model_instance = Question.objects.get(pk=random.randint(1, 100000))
                except Question.DoesNotExist:
                    continue
        else:
            while random_model_instance is None:
                try:
                    random_model_instance = Answer.objects.get(pk=random.randint(1, 1_000_000))
                except Answer.DoesNotExist:
                    continue

        votes = [-1, 1]

        random_user = None

        while random_user is None:
            try:
                random_user = User.objects.get(pk=random.randint(1, 10000))
            except User.DoesNotExist:
                continue

        v = Vote(rate=random.sample(votes, 1)[0], author=random_user, content_object=random_model_instance)
        v.save()
