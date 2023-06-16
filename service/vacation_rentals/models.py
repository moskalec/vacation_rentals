from django.db import models


class RentalProperty(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    availability = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Rental properties"


class RentalBooking(models.Model):
    rental = models.ManyToManyField(RentalProperty, related_name="booked", blank=True)
    user = models.CharField(max_length=255)
    check_in = models.DateField()
    check_out = models.DateField()
