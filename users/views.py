from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from users.services import create_session
from materials.models import Course
from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
import stripe


class PaymentViewSet(viewsets.ModelViewSet):
    """позволяет автоматически реализовать стандартные методы CRUD для модели Payment"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentListView(ListCreateAPIView):
    """позволяет реализовать методы только для получения списка объектов и создания новых объектов"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def perform_create(self, serializer):
        # Извлекаем course_id из тела url запроса
        course_id = self.kwargs.get('course_id')
        # Получаем объект курса по ID
        course = Course.objects.get(id=course_id)
        # Сохраняем платеж с указанием пользователя и оплаченного курса
        payment = serializer.save(user=self.request.user, paid_course=course)

        try:
            course_name = course.title
            session_id, payment_link = create_session(payment.payment_amount, f'к оплате {course_name}')
            payment.session_id = session_id
            payment.payment_link = payment_link
            payment.save()
        except stripe.error.StripeError as e:
            print(f"Ошибка при создании сессии Stripe: {e}")
            raise


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
