"""
URL configuration for studybud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import home, add_questions, get_form, delete, edit_question, practice, check_answer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('add-question/<quiz_id>', add_questions, name='add_questions'),
    path('get-form/<what_form>', get_form, name='get-form'),
    path('edit-question/<ques_id>', edit_question, name='edit_questions'),
    path('practice/<quiz_id>', practice, name='practice'),
    path('check-answers/', check_answer, name='check'),
    path('delete/<type>/<id>', delete, name='delete'),
]
