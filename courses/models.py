from django.db import models
from django.urls import reverse
# Для создания ссылки на объект из таблицы User
from django.contrib.auth.models import User


class Course(models.Model):
    slug = models.SlugField(unique=True)
    # Для создания своего URL адреса.
    # Здесь указываем параметр unique=True и не забываем провести миграции
    # После этого у нас автоматически будет проверка на уникальность этого поля
    # Больше в этом файле ничего не менялось
    title = models.CharField(max_length=120)
    description = models.TextField()
    img = models.ImageField(default='default.jpg',
                            upload_to='course_images')  # Помимо загрузки изоброжений в папку по умолчанию pictures, мы создаём внутри папки новую папку.
    free = models.BooleanField(default=True)

    def __str__(self):  # Магический метод, если мы выводим объект, то для него выводится его название.
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={
            'slug': self.slug})  # При обращении по такому url адресу будет вызывться course/и то значение, которое будет передаваться в поле slug


class Lesson(models.Model):
    slug = models.SlugField()  # Для создания своего URL адреса, название будет плюсоваться к концу ссылки класса Course
    title = models.CharField(max_length=120)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                               null=True)  # Каждый урок будет прикреплён к определённому курсу.
    number = models.IntegerField()
    video_url = models.CharField(max_length=100)

    def __str__(self):  # Если мы обращаемся к этому классу, то выводим title для конкретного объекта
        return self.title

    def get_absolute_url(self):
        return reverse('lesson-detail', kwargs={
            'slug': self.course.slug,
            'lesson_slug': self.slug})  # Сначала обращаемся к курсу, который прикреплён к этому уроку и берём у него slug, а потом обращаемся к slug урока

# Создание новой таблицы
class Comment(models.Model):
    # Три поля: ссылка на автора, ссылка на урок и текст сообщения
    user = models.ForeignKey(User, verbose_name='Пользователь', help_text='Укажите пользователя', on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name='Урок', on_delete=models.SET_NULL, null=True)
    message = models.TextField('Сообщение')

    # Указываем красивые подписи объектов
    def __str__(self):
        return self.lesson.title
