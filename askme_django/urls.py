"""
URL configuration for askme_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from askme_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('signup/', views.sign_up, name="sign_up"),
    path('question/<int:question_id>', views.show_question, name="question"),
    path('tag/<str:title>', views.show_by_tag, name="by_tag"),
    path('hot', views.hot, name="hot_questions"),
    path('ask', views.new_question, name='ask_question'),
    path('admin/', admin.site.urls),
]
