from rest_framework import serializers
from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method')

    def validate(self, data):
        paid_course = data.get('paid_course', getattr(self.instance, 'paid_course', None))
        paid_lesson = data.get('paid_lesson', getattr(self.instance, 'paid_lesson', None))

        if paid_course and paid_lesson:
            raise serializers.ValidationError("Можно оплатить либо курс, либо урок, но не оба одновременно.")
        if not paid_course and not paid_lesson:
            raise serializers.ValidationError("Необходимо указать либо курс, либо урок для оплаты.")
        return data


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'payments')