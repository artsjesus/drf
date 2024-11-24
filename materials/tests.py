from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User
from django.shortcuts import reverse
from rest_framework import status


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test2@dwqdw.ru")
        self.course = Course.objects.create(title="Новый курс", description="Описание")
        self.lesson = Lesson.objects.create(
            title="Новый урок",
            description="Описание",
            video_url="link.youtube.com",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест получения информации об уроке."""
        url = reverse("materials:lesson_get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тест создания нового урока."""
        url = reverse("materials:lesson_create")

        # Корректные данные для создания урока
        data = {
            "title": "Урок 1",
            "course": self.course.pk,
            "description": "Описание",
            "video_url": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)
        # print(response.data)
        # Проверка успешного создания
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

        # Некорректные данные для создания урока
        data = {
            "title": "Урок 1",
            "course": self.course.pk,
            "description": "Описание",
            "video_url": "https://rutube.ru/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update(self):
        """Тест обновления информации об уроке."""
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"title": "Урок 2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок 2")

    def test_lesson_delete(self):
        """Тест удаления урока."""
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест получения списка уроков для курса."""
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.lesson.course.pk,
                    "owner": self.lesson.owner.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@lobster.ru")
        self.course = Course.objects.create(
            title="awgawfawefweaf", description="sefgaesfawe"
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_post(self):
        """Тест подписки на курс."""
        url = reverse("materials:subscribe_view", args=(self.course.pk,))
        data = {"user": self.user.pk, "course_id": self.course.pk}

        self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Подписка добавлена")

    def test_unsubscription_post(self):
        """Тест отписки от курса."""

        # Сначала добавляем подписку (если это необходимо)
        url = reverse("materials:subscribe_view", args=(self.course.pk,))
        data = {"user": self.user.pk, "course_id": self.course.pk}
        self.client.post(url, data)  # Добавление подписки

        # Теперь тестируем отписку
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Подписка удалена")

    def test_subscription_non_existent_course(self):
        """Тест подписки на несуществующий курс."""
        url = reverse("materials:subscribe_view", args=(123123,))
        data = {"user": self.user.pk, "course_id": 123123}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data.get("detail"),
            "No Course matches the given query.",
        )
