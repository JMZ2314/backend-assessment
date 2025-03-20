from django.contrib import admin

from flights.models import Airline, Itinerarie, Leg


@admin.register(Itinerarie)
class ItinerarieAdmin(admin.ModelAdmin):

    list_display = ('id', 'agent', 'price', 'agent_rating', 'legs_summary', 'created_at')
    ordering = ('-created_at',)

    def legs_summary(self, obj):
        legs = obj.legs.all()
        return ", ".join([f"{leg.departure_airport} → {leg.arrival_airport}" for leg in legs])
    
    legs_summary.short_description = 'Legs'


@admin.register(Leg)
class LegAdmin(admin.ModelAdmin):

    list_display = ('id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'stops', 'created_at', 'airline')
    ordering = ('created_at',)

    def airline(self, obj):
        return obj.airline.name
    airline.short_description = 'Airline Name'


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):

    list_display = ('id', 'name','created_at')
    ordering = ('created_at',)
