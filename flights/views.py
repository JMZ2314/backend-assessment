from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from flights.models import Itinerarie
from flights.serializers import ItinerarieSerializer

class ItinerarieListView(ListAPIView):
    
    queryset = Itinerarie.objects.all()
    serializer_class = ItinerarieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        agent = self.request.query_params.get('agent')
        agent_rating = self.request.query_params.get('agent_rating')
        airline_id = self.request.query_params.get('airline_id')

        if agent:
            queryset = queryset.filter(agent__icontains=agent)

        if agent_rating:
            try:
                queryset = queryset.filter(agent_rating__gt=float(agent_rating))
            except ValueError:
                pass 

        if airline_id:
            queryset = queryset.filter(legs__airline_id=airline_id).distinct()

        return queryset
