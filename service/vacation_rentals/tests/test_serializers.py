from django.test import TestCase

from vacation_rentals.models import RentalProperty
from vacation_rentals.serializers import RentalPropertySerializer


class RentalPropertySerializerTestCase(TestCase):
    def test_ok(self):
        rental_property_1 = RentalProperty.objects.create(
            name="test property first",
            location="test location 1",
            price=98.12,
            availability=3,
        )
        rental_property_2 = RentalProperty.objects.create(
            name="test property second",
            location="test location 2",
            price=198.2,
            availability=5,
        )
        data = RentalPropertySerializer(
            [rental_property_1, rental_property_2], many=True
        ).data
        expected_data = [
            {
                "id": rental_property_1.id,
                "name": "test property first",
                "location": "test location 1",
                "price": "98.12",
                "availability": 3,
            },
            {
                "id": rental_property_2.id,
                "name": "test property second",
                "location": "test location 2",
                "price": "198.20",
                "availability": 5,
            },
        ]
        self.assertEquals(expected_data, data)
