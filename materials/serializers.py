from rest_framework import serializers
from .models import Course, Lesson
from .validators import validate_youtube_url
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_url],
        required=False,
        allow_null=True,
    )


    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'preview', 'video_url', 'course')




class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj) -> int:
        return obj.lessons.count()

    def get_is_subscribed(self, obj) -> bool:
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'preview',
            'lessons_count',
            'lessons',
            'is_subscribed',
        )

    def get_lessons_count(self, obj) -> int:
        return obj.lessons.count()

    def get_is_subscribed(self, obj) -> bool:
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()
