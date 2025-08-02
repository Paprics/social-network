from django.urls import path

from . import views

app_name = "geo"

urlpatterns = [
    path("api/countries/", views.get_countries, name="api-countries"),
    path("api/regions/<int:country_id>/", views.get_regions, name="api-regions"),
    path("api/subregions/<int:region_id>/", views.get_subregions, name="api-subregions"),
    path("api/cities/<int:region_id>/", views.get_cities, name="api-cities"),
    path("api/cities_by_subregion/<int:subregion_id>/", views.get_cities_by_subregion, name="api-cities-by-subregion"),
]

# /api/countries/
# /api/countries/<country_id>/regions/
# /api/regions/<region_id>/subregions/
# /api/subregions/<subregion_id>/cities/
