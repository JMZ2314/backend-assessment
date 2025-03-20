from rest_framework import serializers
from .models import Itinerarie,Leg,Airline

class AirlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airline
        fields = ('id','name','created_at',)
        read_only_fields = ('created_at',)

class LegSerializer(serializers.ModelSerializer):

    airline = AirlineSerializer()

    class Meta:
        model = Leg
        fields = ('id', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'stops', 'airline','created_at',)
        read_only_fields = ('created_at',)

class ItinerarieSerializer(serializers.ModelSerializer):

    legs = LegSerializer(many=True)

    class Meta:
        model= Itinerarie
        fields= ('id','price','agent','agent_rating','created_at','legs','created_at',) 
        read_only_fields = ('created_at',)