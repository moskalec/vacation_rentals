from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.db.models import Q

from vacation_rentals.models import RentalProperty
from vacation_rentals.serializers import RentalPropertySerializer


class RentalsFilter(filters.FilterSet):
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains")
    check_in = filters.DateFromToRangeFilter()
    check_out = filters.DateFromToRangeFilter()

    class Meta:
        model = RentalProperty
        exclude = ["id", "price", "availability"]


class RentalPropertyViewSet(ModelViewSet):
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RentalsFilter

    def get_queryset(self):
        check_in = self.request.query_params.get("check_in")
        check_out = self.request.query_params.get("check_out")
        queryset = RentalProperty.objects.all().filter(availability__gt=0)
        if check_in is not None and check_out is not None:
            if check_in > check_out:
                check_in, check_out = check_out, check_in
            return queryset.exclude(
                (Q(booked__check_in__lte=check_in) & Q(booked__check_out__gte=check_in))
                | (
                    Q(booked__check_in__lte=check_out)
                    & Q(booked__check_out__gte=check_out)
                )
                | (
                    Q(booked__check_in__gte=check_in)
                    & Q(booked__check_out__lte=check_out)
                )
            )
