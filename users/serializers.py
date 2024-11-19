from rest_framework.serializers import ModelSerializer
from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """позволяет нам автоматически генерировать сериализацию и десериализацию на основе модели Payment
    также поля для сериализации"""

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_date",
            "paid_course",
            "separately_paid_lesson",
            "payment_amount",
            "payment_method",
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
