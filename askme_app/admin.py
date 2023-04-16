from django.contrib import admin
from askme_app.models import Question, Tag, Vote, Answer, Profile

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(Answer)
admin.site.register(Profile)

# Register your models here.
