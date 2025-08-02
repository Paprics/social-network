from django.http import JsonResponse

from geo.models import City, Country, Region, Subregion


def get_countries(request):
    countries = Country.objects.all().values("id", "name")
    return JsonResponse({"countries": list(countries)})


def get_regions(request, country_id):
    regions = Region.objects.filter(country_id=country_id).values("id", "name")
    return JsonResponse(list(regions), safe=False)


def get_subregions(request, region_id):
    subregions = Subregion.objects.filter(region_id=region_id).values("id", "name")

    print("subregions", subregions)

    return JsonResponse({"subregions": list(subregions)})


def get_cities(request, region_id):
    cities = City.objects.filter(region_id=region_id).values("id", "name")

    print("cities", cities)

    return JsonResponse(list(cities), safe=False)


def get_cities_by_subregion(request, subregion_id):
    cities = City.objects.filter(subregion_id=subregion_id).values("id", "name")
    print("cities by subregion", cities)
    return JsonResponse(list(cities), safe=False)
