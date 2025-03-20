from django.contrib import admin
from django.urls import path
from flights.views import ItinerarieListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/itineraries",ItinerarieListView.as_view(), name='itineraries-list')
]
