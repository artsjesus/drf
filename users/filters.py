import django_filters

from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """ Фильтр для модели Payment"""

    payment_date = django_filters.DateFilter()
    paid_course = django_filters.NumberFilter()
    separately_paid_lesson = django_filters.NumberFilter()
    payment_amount = django_filters.RangeFilter()
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = [
            "payment_date",
            "paid_course",
            "separately_paid_lesson",
            "payment_amount",
            "payment_method",
        ]