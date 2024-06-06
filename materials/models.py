from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="materials/", blank=True, null=True, verbose_name="Превью"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="materials/", blank=True, null=True, verbose_name="Превью"
    )
    link = models.URLField(
        max_length=200, blank=True, null=True, verbose_name="Ссылка на видео"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
