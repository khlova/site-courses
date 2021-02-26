from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'), # класс HomePage обрабатывает главную страницу и её url адресс имеет название home.
    path('tarrifs/', views.tarrifsPage, name='tarrifs'),
    path('callback/', views.callback_payment, name='callback'),
    path('course/<slug>', views.CourseDetailPage.as_view(), name='course-detail'),# у каждого курса окончание ссылки будет меняться по полю slug из БД, а начало ссылки course - статично
    path('course/<slug>/<lesson_slug>', views.LessonDetailPage.as_view(), name='lesson-detail'), # course/android/set-up
    path('add-course', views.CourseAdd.as_view(), name='course-add')  # Прописываем отслеживание формы добавления курсов.
]
