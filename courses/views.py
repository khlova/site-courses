from django.shortcuts import render, redirect # Подключаем метод для переадресации
from .forms import CommentForm # Подключаем класс формы для Comment
from .models import Course, Lesson, Comment
from django.views.generic import ListView, DetailView, CreateView
from .forms import CourseAddForm  # Импортирован класс CourseAddForm для создания формы
from cloudipsp import Api, Checkout
import time, json


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'  # Имя шаблона, который будет обрабатывать данную страницу.
    context_object_name = 'courses'  # Указываем из какой таблицы в БД мы будем вытягивать все данные.
    ordering = [
        '-id']  # Сортировка в обратном порядке, т.е. сначала будут отображаться записи, которые были добавлены самыми последними.

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(
            **kwargs)  # Создаём объект. Обращаемся к основному классу ListView, передаём в него наш класс и вызываем функцию в которую передаём дополнительные параметры, которые получаем.
        ctx[
            'title'] = 'Главная страница сайта'  # В этом словаре будут находитбся разные элементы, которые мы будем передавать в шаблон.
        return ctx


def callback_payment(
        request):  # Получаем все данные которые будут переданы от сервиса оплаты (фонди), внутри этого метода можно прописать любой функционал, например, отправка письма на почту, шаблон не нужно выводить.
    if request.method == 'POST':
        data = json.load(request.POST)
        print(data)


def tarrifsPage(request):
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": 150000,
        "order_desc": 'Покупка подписки на сайте',
        "order_id": str(time.time()),
        'merchant_data': 'example@itproger.com'  # Получаем дополнительные данные из объекта data по методу POStT

    }
    url = checkout.url(data).get('checkout_url')
    return render(request, 'courses/tarrifs.html', {'title': 'Тарифы на сайт', 'url': url})


class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(
            **kwargs)
        ctx['title'] = Course.objects.filter(slug=self.kwargs[
            'slug']).first()  # Берём название у курса и подставляем в название ярлыка стр. Т.е. фильтруем объекты, ищем объект у котоорого поле slug точно такое же как и значение конечной записи в url. Выбыираем только 1 объект.
        ctx['lessons'] = Lesson.objects.filter(course=ctx['title']).order_by(
            'number')  # Фильтруем и находим все уроки у которых поле курс будет точно таким же как и название курса на стр. кот. мы сейчас находимся. Сортируем по номеру урока.

        # print(ctx['lessons'].query) # Проверка правильности написания фильтра (SQL).
        return ctx


class LessonDetailPage(DetailView):
    model = Course
    template_name = 'courses/lessons-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(
            **kwargs)
        course = Course.objects.filter(slug=self.kwargs[
            'slug']).first()  # Получаем курс на страничке которого сейчас находимся
        lesson = list(Lesson.objects.filter(course=course).filter(slug=self.kwargs[
            'lesson_slug']).values())  # Находим уроки на стр курса которого мы находимся. И плюс у которых значение slug, такое же как в url. В конце получаем все значения из БД и записываем их в переменную lesson. Нужно обернуть в список, чтобы не работать с QuerySet
                # Передаем в шаблон все комментарии, что соответсвуют id записи, на которой мы находимся
        comments = Comment.objects.filter(lesson=lesson[0]['id']).all()
        ctx['comments'] = comments
        # Также передаем форму в шаблон
        ctx['commForm'] = CommentForm()

        # print(lesson)
        ctx['title'] = lesson[0]['title']  # Обращаемся к 1 элементу и берём название урока
        ctx['desc'] = lesson[0]['description']
        ctx['video'] = lesson[0]['video_url'].split("=")[
            1]  # Обрезаем ссылку на видео до = и после, нам нужно только id видео, оно после =, берём 1 элемент.
        return ctx

# Этот метод срабатывает при отправке данных из формы
    def post(self, request, *args, **kwargs):
        # Получаем курс и получаем текущий урок
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = Lesson.objects.filter(course=course).filter(slug=self.kwargs['lesson_slug']).first()

        post = request.POST.copy() # Копируем POST данные прежде, чем их валидировать
        post['user'] = request.user # Устаналвиаем свои данные – указываем авторизованного пользователя
        post['lesson'] = lesson # Указываем урок, на котором сейчас находимся
        request.POST = post # Меняем request.POST данные на новые, измененные данные

        # Создаем объект на основе класса формы
        form = CommentForm(request.POST)
        if form.is_valid(): # Проверяем его
            form.save() # Сохраняем новый комментарий

        # Выполняем переадресацию
        url = self.kwargs['slug'] + '/' + self.kwargs['lesson_slug']

        return redirect('/course/' + url)

class CourseAdd(CreateView):  # В этом классе все наследуем от CreateView
    form_class = CourseAddForm  # Остается лишь указать форму что будет показана,
    template_name = 'courses/course_form.html'  # а также шаблон, что будет использован для формы
