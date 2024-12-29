from django.contrib import admin
from django.urls import path, include
from .views import home, add_questions, get_form, delete, edit_question, practice, check_answer, report
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # type: ignore
    path('add-question/<quiz_id>', add_questions, name='add_questions'),
    path('get-form/<what_form>', get_form, name='get-form'),
    path('edit-question/<ques_id>', edit_question, name='edit_questions'),
    path('practice/<quiz_id>', practice, name='practice'),
    path('check-answers/', check_answer, name='check'),
    path('report/<quiz_id>', report, name='report'), # type: ignore
    path('delete/<type>/<id>', delete, name='delete'), # type: ignore
    path('auth/', include('simple.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
