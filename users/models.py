from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Subject

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Телефон")
    city = models.CharField(max_length=80, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/", blank=True, null=True, verbose_name="Аватар")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платежей"""
    cash = "Наличные"
    transfer = "Перевод на счёт"
    payment_methods = [(cash, "Наличные"), (transfer, "Перевод на счёт")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Пользователь")
    payment_date = models.DateField(verbose_name="Дата оплаты")
    course_paid = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="Оплаченный курс")
    subject_paid = models.ForeignKey(Subject, on_delete=models.CASCADE, **NULLABLE, verbose_name="Оплаченный урок")
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=50, default=transfer, choices=payment_methods)
    payment_id = models.CharField(max_length=255, **NULLABLE, verbose_name='id платежа')
    payment_link = models.URLField(max_length=400, **NULLABLE, verbose_name='Ссылка на оплату')
    payment_status = models.URLField(max_length=400, **NULLABLE, verbose_name='Статус платежа')

    def __str__(self):
        return f"У {self.user} дата оплаты {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
