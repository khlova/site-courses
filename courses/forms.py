from django import forms
from .models import Course, Comment


# Создаем класс для отображения формы
class CourseAddForm(forms.ModelForm):
    # Указываем что поле img будет необязательным,
    # остальные по-умолчанию обязательные
    img = forms.ImageField(required=False)

    def __init__(self, *args, **kwards):
        super(CourseAddForm, self).__init__(*args, **kwards)
        # Переопределяем названия полей
        self.fields['slug'].label = "Название URL"
        self.fields['title'].label = "Название курса"
        self.fields['description'].label = "Описание курса"
        self.fields['img'].label = "Изображение профиля"

    class Meta:
        # Указываем модель и выводим поля в форме
        model = Course
        fields = ['slug', 'title', 'description', 'img']

# Указываем класс формы
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Мы будем работать со всеми полями
        fields = ['message', 'user', 'lesson']

        # При этом поля user и lesson отображать на странице мы не будем
        widgets = {'user': forms.HiddenInput(), 'lesson': forms.HiddenInput()}    

