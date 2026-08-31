from rest_framework.test import APITestCase

from .models import Course, Lesson


class CourseDetailAPITest(APITestCase):
	def test_retrieve_course_returns_lessons_count_and_lessons(self):
		course = Course.objects.create(title='Django')
		Lesson.objects.create(course=course, title='Models')
		Lesson.objects.create(course=course, title='Views')

		response = self.client.get(f'/api/courses/{course.id}/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['lessons_count'], 2)
		self.assertEqual(len(response.data['lessons']), 2)
