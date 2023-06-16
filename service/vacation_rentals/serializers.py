from rest_framework.serializers import ModelSerializer

from vacation_rentals.models import RentalProperty


class RentalPropertySerializer(ModelSerializer):
    class Meta:
        model = RentalProperty
        fields = "__all__"
