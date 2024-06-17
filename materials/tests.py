from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from materials.models import Course, Subject
from users.models import User


class CourseTestCase(APITestCase):
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

    def test_create_course(self):
        """Тестирование на создание курса"""
        data = {
            "name": self.course.name,
            "description": self.course.description,
        }
        response = self.client.post("/materials/course/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Course.objects.all().exists())

    # Работает только без пагинации
    def test_list_course(self):
        """Тестирование на вывод списка курсов"""

        response = self.client.get(
            "/materials/course/",
        )
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "Управление IT-продуктом",
                        "description": "Управление IT-продуктом",
                        "preview": None,
                        "owner": None,
                        "subscription": False,
                        "subject": [
                            {
                                "id": 4,
                                "name": "Риск-менеджмент",
                                "description": "Риск-менеджмент",
                                "preview": None,
                                "link": None,
                                "course": 5,
                                "owner": 4,
                            }
                        ],
                        "subject_count": 1,
                    }
                ],
            },
        )

    def test_detail_course(self):
        """Тестирование на просмотр одного курса"""
        data = {
            "name": self.course.name,
            "description": self.course.description,
        }
        response = self.client.get(f"/materials/course/{self.course.id}/", data=data)

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

        data = {
            "name": "delete test",
            "description": "delete test",
        }
        response = self.client.delete(f"/materials/course/{self.course.id}/", data=data)
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
        response = self.client.post("/materials/subject/create", data=data)

        self.assertTrue(Subject.objects.all().exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_subject(self):
        """Тестирование на вывод списка предметов"""

        response = self.client.get(
            "/materials/subject/",
        )

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

        data = {
            "name": self.subject.name,
            "description": self.subject.description,
        }
        response = self.client.get(
            f"/materials/subject/detail/{self.subject.id}", data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_subject(self):
        """Тестирование на обновление предмета"""
        data = {
            "name": "Управление проектами",
            "description": "Управление проектами",
            "course": self.course.id,
            "owner": self.user.id,
        }
        response = self.client.patch(f"/materials/subject/edit/{self.subject.id}", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, data["name"])
        self.assertEqual(self.subject.description, data["description"])

    def test_delete_subject(self):
        """Тестирование на удаление предмета"""

        data = {
            "name": "delete test",
            "description": "delete test",
        }
        response = self.client.delete(
            f"/materials/subject/delete/{self.subject.id}", data
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
