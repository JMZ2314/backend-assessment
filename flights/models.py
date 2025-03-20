from django.db import models

# Create your models here.

class Airline (models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Leg(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    departure_airport = models.CharField(max_length=3)  
    arrival_airport = models.CharField(max_length=3)    
    departure_time = models.DateTimeField()             
    arrival_time = models.DateTimeField()               
    stops = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    airline = models.ForeignKey(Airline,on_delete=models.CASCADE,related_name="legs")

class Itinerarie(models.Model):
    id = models.CharField(primary_key=True,max_length=20)
    price = models.CharField(max_length=5)
    agent = models.CharField(max_length=20)
    agent_rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    legs = models.ManyToManyField(Leg,related_name="itineraries")