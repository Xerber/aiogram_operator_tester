from django.contrib import admin
from .models import Category, Question, Test_levels, Test_question_qty, Test, Test_answer



# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
  list_display = ("category","diff_level","body")
  list_filter = ("category__title","diff_level")


class QuestionInline(admin.TabularInline):
    '''Вывод списка вопросов внутри категории'''
    model = Question
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  inlines = [QuestionInline,]


class TestQuestionQtyInline(admin.TabularInline):
    '''Настройка количества вопросов в категории'''
    model = Test_question_qty
    extra = 0


@admin.register(Test_levels)
class TestLevelsAdmin(admin.ModelAdmin):
  inlines = [TestQuestionQtyInline,]


class TestAnswerInline(admin.TabularInline):
    '''Ответы на пройденные тесты'''
    model = Test_answer
    extra = 0


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
  inlines = [TestAnswerInline,]

