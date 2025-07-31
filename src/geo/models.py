from django.db import models


class Country(models.Model):
    # Названия
    name = models.CharField(max_length=200, verbose_name="Название (EN)")
    name_ascii = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название ASCII")
    name_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название (RU)")
    name_uk = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название (UK)")

    # Коды страны
    code2 = models.CharField(max_length=2, unique=True, verbose_name="ISO2 код")  # AL, RU, UA
    code3 = models.CharField(max_length=3, blank=True, null=True, verbose_name="ISO3 код")  # ALB, RUS, UKR
    code = models.CharField(max_length=3, blank=True, null=True, verbose_name="ISO-код (кастомный)")

    # Телефонные коды
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name="Телефонный код")  # 355, 7, 380
    phone_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Телефонный код (альтернативный)")

    # GeoNames и прочее
    slug = models.SlugField(unique=True)
    geoname_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="GeoName ID")
    alternate_names = models.TextField(blank=True, null=True, verbose_name="Альтернативные имена")
    continent = models.CharField(max_length=2, blank=True, null=True, verbose_name="Континент (код)")
    tld = models.CharField(max_length=5, blank=True, null=True, verbose_name="Домен верхнего уровня")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name_ru or self.name_uk or self.name


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")

    # Названия
    name = models.CharField(max_length=200, verbose_name="Название (EN)")
    name_ascii = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название ASCII")
    name_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название (RU)")
    name_uk = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название (UK)")

    # GeoNames
    slug = models.SlugField()
    geoname_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="GeoName ID")
    alternate_names = models.TextField(blank=True, null=True, verbose_name="Альтернативные имена")
    display_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Отображаемое имя")
    geoname_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"

    def __str__(self):
        return self.name_ru or self.name_uk or self.name


class Subregion(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="subregions")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="subregions", blank=True, null=True)

    # Названия
    name = models.CharField(max_length=200)
    name_ascii = models.CharField(max_length=200, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    # GeoNames
    slug = models.SlugField(max_length=255, blank=True, null=True)
    geoname_id = models.BigIntegerField(blank=True, null=True)
    geoname_code = models.CharField(max_length=50, blank=True, null=True)

    # Прочее
    alternate_names = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)  # ISO или иной код
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"

    def __str__(self):
        return self.display_name or self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities", blank=True, null=True)
    subregion = models.ForeignKey(Subregion, on_delete=models.CASCADE, related_name="cities", blank=True, null=True)

    # Названия
    name = models.CharField(max_length=200, verbose_name="Название (EN)")
    name_ascii = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название ASCII")
    name_ru = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название (RU)")
    name_uk = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название (UK)")

    # GeoNames
    slug = models.SlugField()
    geoname_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="GeoName ID")
    alternate_names = models.TextField(blank=True, null=True, verbose_name="Альтернативные имена")

    # Доп. инфа
    population = models.PositiveIntegerField(blank=True, null=True, verbose_name="Население")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    search_names = models.TextField(blank=True, null=True)
    feature_code = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name_ru or self.name_uk or self.name
