from django.contrib import admin

from .models import City, Country, Region, Subregion

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Subregion)
admin.site.register(City)
