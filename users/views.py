from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView

from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import PaymentSerializer


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
