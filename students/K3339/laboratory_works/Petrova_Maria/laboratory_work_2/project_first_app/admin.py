from django.contrib import admin

from .models import (
    Hotel,
    RoomType,
    Amenity,
    Room,
    Reservation,
    Review,
    Stay,
)


admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Amenity)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Review)


@admin.register(Stay)
class StayAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'room',
        'check_in',
        'check_out',
    )

    list_filter = (
        'room',
        'check_in',
    )

    search_fields = (
        'user__username',
        'room__number',
    )