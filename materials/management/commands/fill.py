from django.core.management import BaseCommand

from materials.models import Course, Subject
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payment.objects.all().delete()

        payment_list = [
            {
                "user": User.objects.get(email="student1@mail.ru"),
                "payment_date": "2024-06-09",
                "course_paid": Course.objects.get(name="IT"),
                "subject_paid": Subject.objects.get(name="Python"),
                "payment_amount": "1500",
                "payment_method": "Наличные",
            },
            {
                "user": User.objects.get(email="student2@mail.ru"),
                "payment_date": "2024-06-05",
                "course_paid": Course.objects.get(name="IT"),
                "subject_paid": Subject.objects.get(name="HTML"),
                "payment_amount": "1000",
                "payment_method": "Перевод на счёт",
            },
        ]

        payments = []

        for payment in payment_list:
            payments.append(Payment(**payment))

        Payment.objects.bulk_create(payments)
