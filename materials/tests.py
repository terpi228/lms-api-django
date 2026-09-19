from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from .models import Course, Lesson
from .serializers import LessonSerializer


class CourseDetailAPITest(APITestCase):
	def test_retrieve_course_returns_lessons_count_and_lessons(self):
		course = Course.objects.create(title='Django')
		Lesson.objects.create(course=course, title='Models')
		Lesson.objects.create(course=course, title='Views')

		response = self.client.get(f'/api/courses/{course.id}/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['lessons_count'], 2)
		self.assertEqual(len(response.data['lessons']), 2)

	def test_course_list_is_paginated(self):
		Course.objects.bulk_create(
			[Course(title=f'Course {index}') for index in range(11)]
		)

		response = self.client.get('/api/courses/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 11)
		self.assertEqual(len(response.data['results']), 10)

		response = self.client.get('/api/courses/?page_size=3')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data['results']), 3)

	def test_lesson_serializer_rejects_non_youtube_url(self):
		serializer = LessonSerializer(data={
			'title': 'Lesson',
			'course': 1,
			'video_url': 'https://example.com/video',
		})

		self.assertFalse(serializer.is_valid())
		self.assertIn('video_url', serializer.errors)


class LessonCRUDPermissionsAPITest(APITestCase):
	def setUp(self):
		self.owner = self._create_user('owner@example.com', 'owner')
		self.other_user = self._create_user('other@example.com', 'other')
		self.moderator = self._create_user('moderator@example.com', 'moderator')
		moderators = Group.objects.create(name='moderators')
		moderators.user_set.add(self.moderator)
		self.course = Course.objects.create(title='Django', owner=self.owner)
		self.lesson = Lesson.objects.create(
			course=self.course,
			title='Models',
			owner=self.owner,
		)

	def _create_user(self, email, username):
		from users.models import User

		return User.objects.create_user(
			email=email,
			username=username,
			password='password',
		)

	def test_owner_can_create_update_and_delete_lesson(self):
		self.client.force_authenticate(user=self.owner)

		create_response = self.client.post('/api/lessons/', {
			'title': 'Views',
			'course': self.course.id,
			'video_url': 'https://www.youtube.com/watch?v=test',
		}, format='json')
		self.assertEqual(create_response.status_code, 201)

		update_response = self.client.patch(
			f'/api/lessons/{self.lesson.id}/',
			{'title': 'Updated models'},
			format='json',
		)
		self.assertEqual(update_response.status_code, 200)

		delete_response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
		self.assertEqual(delete_response.status_code, 204)

	def test_moderator_can_update_but_cannot_create_or_delete_lesson(self):
		self.client.force_authenticate(user=self.moderator)

		update_response = self.client.patch(
			f'/api/lessons/{self.lesson.id}/',
			{'title': 'Moderated lesson'},
			format='json',
		)
		self.assertEqual(update_response.status_code, 200)

		create_response = self.client.post('/api/lessons/', {
			'title': 'Forbidden lesson',
			'course': self.course.id,
		}, format='json')
		self.assertEqual(create_response.status_code, 403)

		delete_response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
		self.assertEqual(delete_response.status_code, 403)

	def test_other_user_cannot_modify_lesson(self):
		self.client.force_authenticate(user=self.other_user)

		response = self.client.patch(
			f'/api/lessons/{self.lesson.id}/',
			{'title': 'Invalid update'},
			format='json',
		)
		self.assertEqual(response.status_code, 404)
