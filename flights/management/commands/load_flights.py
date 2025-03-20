import requests
from django.utils.timezone import make_aware
from datetime import datetime
from django.core.management.base import BaseCommand
from flights.models import Itinerarie,Airline,Leg

class Command(BaseCommand):

    help = 'Inicializar la vase de datos desde https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json'

    def handle(self, *args, **kwargs):

        if(Itinerarie.objects.exists() or Leg.objects.exists() or Airline.objects.exists()):
            self.stdout.write(self.style.WARNING('La base de datos ya tiene data'))
            return

        try:
            response = requests.get("https://raw.githubusercontent.com/Skyscanner/full-stack-recruitment-test/main/public/flights.json")
            data = response.json()

            self.stdout.write(self.style.SUCCESS('Data obtenida exitosamente'))
    
            itineraries = []
            legs = []
            airlines = {}
            itinerary_leg= []


            # Obtener la aerolíneas
            for leg_fecth in data["legs"]:
                if leg_fecth["airline_id"] not in airlines:
                    airlines[leg_fecth["airline_id"]] = Airline(
                        id= leg_fecth["airline_id"],
                        name= leg_fecth["airline_name"]
                    )

            # Obtener los tramos
            for leg_fecth in data["legs"]:

                leg = Leg(
                    id=leg_fecth["id"],
                    departure_airport= leg_fecth["departure_airport"],
                    arrival_airport= leg_fecth["arrival_airport"],
                    departure_time= make_aware(datetime.fromisoformat(leg_fecth["departure_time"])),
                    arrival_time= make_aware(datetime.fromisoformat(leg_fecth["arrival_time"])),
                    stops= leg_fecth["stops"],
                    airline= airlines[leg_fecth["airline_id"]],
                )
                legs.append(leg)

            #Obtener los itinerarios
            for itinerary_fetch in data["itineraries"]:
                itinerary = Itinerarie(
                    id= itinerary_fetch["id"],
                    price= itinerary_fetch["price"],
                    agent= itinerary_fetch["agent"],
                    agent_rating= itinerary_fetch["agent_rating"],
                )
                itineraries.append(itinerary)

                for leg_id in itinerary_fetch["legs"]:
                    itinerary_leg.append((itinerary, leg_id))

            # Inserciones masivas
            self.stdout.write("Creando areolíneas...")
            Airline.objects.bulk_create(airlines.values(), ignore_conflicts=True)

            self.stdout.write("Creando tramos...")
            Leg.objects.bulk_create(legs, ignore_conflicts=True)

            self.stdout.write("Creando itinerarios...")
            Itinerarie.objects.bulk_create(itineraries, ignore_conflicts=True)

            # Crear relaciones Many-to-Many
            self.stdout.write("Creando relaciones...")
            for itinerary, leg_id in itinerary_leg:
                itinerary.legs.add(Leg.objects.get(id=leg_id))

            self.stdout.write(self.style.SUCCESS('Base de datos inicializada'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ha ocurrido un error al inicializar la base de datos: {e}'))



