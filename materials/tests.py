from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from materials.models import Course, Subject, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", password="123qwer")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Управление IT-продуктом", description="Управление IT-продуктом", owner=self.user
        )
        self.subject = Subject.objects.create(
            name="Риск-менеджмент",
            description="Риск-менеджмент",
            course=self.course,
            owner=self.user,
        )

    def test_create_course(self):
        """Тестирование на создание курса"""
        data = {
            "name": "Тестовый курс 1",
            "description": "Тестовое описание курса",
        }
        response = self.client.post("/materials/course/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json(), {"name": "Тестовый курс 1",
                                          "description": "Тестовое описание курса"})

    # Работает только без пагинации
    def test_list_course(self):
        """Тестирование на вывод списка курсов"""

        response = self.client.get(
            "/materials/course/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             "count": 1,
                             "next": None,
                             "previous": None,
                             "results": [
                                 {
                                     "id": self.course.pk,
                                     "subject_count": 1,
                                     "subject": [{
                                         "id": self.subject.pk,
                                         "name": "Риск-менеджмент",
                                         "description": "Риск-менеджмент",
                                         "preview": None,
                                         "link": None,
                                         "course": self.course.pk,
                                         "owner": self.user.pk}],
                                     "subscription": False,
                                     "name": "Управление IT-продуктом",
                                     "description": "Управление IT-продуктом",
                                     "preview": None,
                                     "owner": self.user.pk
                                 }
                             ]
                         }
                         )

    def test_detail_course(self):
        """Тестирование на просмотр одного курса"""

        response = self.client.get(f"/materials/course/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        """Тестирование на обновлении курса"""
        data = {
            "name": "update test",
            "description": "update test",
        }
        response = self.client.patch(f"/materials/course/{self.course.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, data["name"])
        self.assertEqual(self.course.description, data["description"])

    def test_delete_course(self):
        """Тестирование на удаление курса"""

        response = self.client.delete(f"/materials/course/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubjectTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", password="123qwer")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Управление IT-продуктом", description="Управление IT-продуктом"
        )
        self.subject = Subject.objects.create(
            name="Риск-менеджмент",
            description="Риск-менеджмент",
            course=self.course,
            owner=self.user,
        )

    def test_create_subject(self):
        """Тестирование на создание предмета"""

        data = {
            "name": self.subject.name,
            "description": self.subject.description,
            "course": self.course.id,
            "link": "https://youtube.com/",
        }
        response = self.client.post(reverse("materials:subjects_create"), data=data)

        self.assertTrue(Subject.objects.all().exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_subject(self):
        """Тестирование на вывод списка предметов"""

        response = self.client.get(reverse("materials:subjects_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.subject.id,
                        "name": "Риск-менеджмент",
                        "description": "Риск-менеджмент",
                        "preview": None,
                        "link": None,
                        "course": self.course.id,
                        "owner": self.user.id,
                    }
                ],
            },
        )

    def test_detail_subject(self):
        """Тестирование на просмотр одного предмета"""

        response = self.client.get(reverse("materials:subjects_detail",
                                           kwargs={"pk": self.subject.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_subject(self):
        """Тестирование на обновление предмета"""
        data = {
            "name": "Управление проектами",
            "description": "Управление проектами",
            "course": self.course.id,
            "owner": self.user.id,
        }
        response = self.client.patch(reverse("materials:subjects_edit",
                                             kwargs={"pk": self.subject.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, data["name"])
        self.assertEqual(self.subject.description, data["description"])

    def test_delete_subject(self):
        """Тестирование на удаление предмета"""

        response = self.client.delete(reverse("materials:subjects_delete", kwargs={"pk": self.subject.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="test@mail.ru", password="123qwer")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="Курс", description="Тестовый курс", owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_subscription(self):
        data = {"user": self.user.pk,
                "course": self.course.pk}

        response = self.client.post(reverse('materials:subscription_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка удалена"})

        response = self.client.post(reverse('materials:subscription_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка добавлена"})
