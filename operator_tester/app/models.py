from django.db import models


# Create your models here.
class Category(models.Model):
    '''Категории вопросов'''
    title = models.CharField('Название', max_length=100)

    def __str__(self):
      return self.title
    
    class Meta:
      verbose_name = "Категория"
      verbose_name_plural = "Категории"


Difficulty_level = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]

class Question(models.Model):
    '''Вопросы'''
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    diff_level = models.CharField('Сложность вопроса', choices=Difficulty_level, max_length=6)
    body = models.TextField('Вопрос', max_length=500)

    def __str__(self):
      return self.body[:15]
    
    class Meta:
      verbose_name = "Вопрос"
      verbose_name_plural = "Вопросы"


class Test_levels(models.Model):
    '''Создание теста'''
    title = models.CharField('Название', max_length=100)

    def __str__(self):
      return self.title
    
    class Meta:
      verbose_name = "Создание теста"
      verbose_name_plural = "Создание тестов"


class Test_question_qty(models.Model):
    '''Настройка количества вопросов в категориях'''
    title = models.ForeignKey(Test_levels, verbose_name='Тест', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    qty_easy = models.PositiveSmallIntegerField('Количество "легких" вопросов', default=0)
    qty_medium = models.PositiveSmallIntegerField('Количество "средних" вопросов', default=0)
    qty_hard = models.PositiveSmallIntegerField('Количество "сложных" вопросов', default=0)

    def __str__(self):
      return f'{self.title} | {self.category}'
    
    class Meta:
      verbose_name = "Вопросов в категории"
      verbose_name_plural = "Вопросов в категориях"


class Test(models.Model):
    '''Пройденные тесты с краткой информацией'''
    uid = models.CharField(primary_key=True, unique=True, editable=False, max_length=255)
    name = models.CharField('Имя опрашиваемого', max_length=255)
    test_level = models.ForeignKey(Test_levels, verbose_name='Название теста', on_delete=models.DO_NOTHING)
    grade = models.PositiveSmallIntegerField('Оценка')
    datetime = models.DateTimeField('Дата сдачи', auto_created=True)

    def __str__(self):
      return f'{self.name} | {self.datetime}'
    
    class Meta:
      verbose_name = "Пройденный тест"
      verbose_name_plural = "Пройденные тесты"


class Test_answer(models.Model):
    '''Ответы на пройденные тесты'''
    uid = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField('Вопрос', max_length=500)
    grade = models.PositiveSmallIntegerField('Оценка')

    def __str__(self):
      return f'{self.question[:15]} | {self.grade}'
    
    class Meta:
      verbose_name = "Ответ на пройденный тест"
      verbose_name_plural = "Ответов на пройденные тесты"