from django.contrib import admin
from django.contrib.admin import ModelAdmin

from vacation_rentals.models import RentalProperty, RentalBooking


@admin.register(RentalProperty)
class RentalPropertyAdmin(ModelAdmin):
    list_display = ["name", "location", "price", "availability"]


@admin.register(RentalBooking)
class RentalPropertyAdmin(ModelAdmin):
    list_display = ["user", "check_in", "check_out"]
