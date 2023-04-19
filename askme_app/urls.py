from django.urls import path
from askme_app import views

urlpatterns = [
    path('question/<int:question_id>', views.show_question, name="question"),
    path('tag/<str:title>', views.show_by_tag, name="by_tag"),
    path('hot/', views.hot, name="hot_questions"),
    path('ask/', views.new_question, name='ask_question'),
]
