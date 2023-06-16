from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from vacation_rentals.models import RentalProperty, RentalBooking
from vacation_rentals.serializers import RentalPropertySerializer


class RentalPropertyApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.rental_property_1 = RentalProperty.objects.create(
            name="Crowne Plaza Times Square Manhattan, an IHG Hotel",
            location="1605 Broadway Avenue, New York, NY 10019, United States –",
            price=86.12,
            availability=3,
        )
        self.rental_property_2 = RentalProperty.objects.create(
            name="Hyatt Place New York City/Times Square",
            location="350 West 39th St, Hell's Kitchen, New York, NY 10018, United States",
            price=98.2,
            availability=5,
        )
        self.rental_property_3 = RentalProperty.objects.create(
            name="TBA Times Square",
            location="340 West 40th Street, Hell's Kitchen, New York, NY 10018, United States",
            price=89.2,
            availability=4,
        )
        self.rental_property_4 = RentalProperty.objects.create(
            name="The Herald by LuxUrban",
            location="71 West 35th Street, New York, NY 10001, United States",
            price=78.2,
            availability=5,
        )

        self.rental_booking_1 = RentalBooking.objects.create(
            user="Oliver Smith",
            check_in="2023-06-03",
            check_out="2023-06-07",
        )
        self.rental_booking_1.rental.add(self.rental_property_4)

        self.rental_booking_2 = RentalBooking.objects.create(
            user="Emily Williams",
            check_in="2023-06-11",
            check_out="2023-06-13",
        )
        self.rental_booking_2.rental.add(self.rental_property_3)

    def test_get(self):
        url = reverse("rental-list")
        response = self.client.get(url)
        serializer_data = RentalPropertySerializer(
            [
                self.rental_property_1,
                self.rental_property_2,
                self.rental_property_3,
                self.rental_property_4,
            ],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter_name(self):
        url = reverse("rental-list")
        response = self.client.get(url, data={"name": "Crowne"})
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1], many=True
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(url, data={"name": "Times"})
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2, self.rental_property_3],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter_location(self):
        url = reverse("rental-list")
        response = self.client.get(
            url,
            data={"location": "71 West 35th Street, New York, NY 10001, United States"},
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_4], many=True
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(url, data={"location": "NY 10018"})
        serializer_data = RentalPropertySerializer(
            [self.rental_property_2, self.rental_property_3], many=True
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter_max_price(self):
        url = reverse("rental-list")
        response = self.client.get(url, data={"max_price": 90})
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_3, self.rental_property_4],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(url, data={"max_price": 80})
        serializer_data = RentalPropertySerializer(
            [self.rental_property_4], many=True
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter_check_in(self):
        url = reverse("rental-list")
        response = self.client.get(url, data={"check_in": "2023-01-01"})
        serializer_data = RentalPropertySerializer(
            [
                self.rental_property_1,
                self.rental_property_2,
                self.rental_property_3,
                self.rental_property_4,
            ],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(url, data={"check_in": "2023-06-04"})
        serializer_data = RentalPropertySerializer(
            [
                self.rental_property_1,
                self.rental_property_2,
                self.rental_property_3,
                self.rental_property_4,
            ],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter_check_out(self):
        url = reverse("rental-list")
        response = self.client.get(url, data={"check_out": "2023-01-01"})
        serializer_data = RentalPropertySerializer(
            [
                self.rental_property_1,
                self.rental_property_2,
                self.rental_property_3,
                self.rental_property_4,
            ],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(url, data={"check_out": "2023-06-05"})
        serializer_data = RentalPropertySerializer(
            [
                self.rental_property_1,
                self.rental_property_2,
                self.rental_property_3,
                self.rental_property_4,
            ],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

    def test_get_filter_check_in_out(self):
        url = reverse("rental-list")
        response = self.client.get(
            url, data={"check_in": "2023-01-01", "check_out": "2023-01-10"}
        )
        serializer_data = RentalPropertySerializer(
            [
                self.rental_property_1,
                self.rental_property_2,
                self.rental_property_3,
                self.rental_property_4,
            ],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(
            url, data={"check_in": "2023-06-03", "check_out": "2023-06-07"}
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2, self.rental_property_3],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(
            url, data={"check_in": "2023-06-06", "check_out": "2023-06-09"}
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2, self.rental_property_3],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(
            url, data={"check_in": "2023-06-01", "check_out": "2023-06-05"}
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2, self.rental_property_3],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(
            url, data={"check_in": "2023-06-01", "check_out": "2023-06-10"}
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2, self.rental_property_3],
            many=True,
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(
            url, data={"check_in": "2023-06-05", "check_out": "2023-06-15"}
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2], many=True
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)

        response = self.client.get(
            url, data={"check_in": "2023-06-15", "check_out": "2023-06-05"}
        )
        serializer_data = RentalPropertySerializer(
            [self.rental_property_1, self.rental_property_2], many=True
        ).data
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serializer_data, response.data)
