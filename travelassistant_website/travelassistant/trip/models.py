from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.urlresolvers import reverse
# from django.
# Create your models here.
# trip  model.py file
# from accounts.models import Users
# User = get_user_model()

# from accounts.models import Users
from django.urls import reverse
# Inherit the Users modles from accounts.models
# class Users(Users):
#     pass

class Accommodations(models.Model):
    accommodation_id = models.IntegerField(primary_key=True)
    ac_name = models.CharField(max_length=255)
    county = models.CharField(max_length=255, blank=True, null=True)
    city_name = models.ForeignKey('City', models.DO_NOTHING, db_column='city_name')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    avg_rating = models.FloatField(blank=True, null=True)
    price_level = models.CharField(max_length=5, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    bathroom = models.CharField(max_length=45, blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    beds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accommodations'

    def get_absolute_url(self):
        return reverse("travel:accommodations-detail", kwargs={"my_id": self.id})

class Attractions(models.Model):
    attraction_id = models.IntegerField(primary_key=True)
    ranking = models.IntegerField(blank=True, null=True)
    city_name = models.ForeignKey('City', models.DO_NOTHING, db_column='city_name', blank=True, null=True)
    a_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    a_address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attractions'

    def get_absolute_url(self):
        return reverse("travel:attractions-detail", kwargs={"my_id": self.id})

class City(models.Model):
    city_name = models.CharField(primary_key=True, max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'

class Laundry(models.Model):
    laundry_id = models.IntegerField(primary_key=True)
    l_name = models.CharField(max_length=255, blank=True, null=True)
    city_name = models.ForeignKey(City, models.DO_NOTHING, db_column='city_name', blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    l_address = models.CharField(max_length=255, blank=True, null=True)
    price_range = models.CharField(max_length=5, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'laundry'

class Markets(models.Model):
    market_id = models.IntegerField(primary_key=True)
    city_name = models.ForeignKey(City, models.DO_NOTHING, db_column='city_name')
    m_name = models.CharField(max_length=255, blank=True, null=True)
    avg_rating = models.FloatField(blank=True, null=True)
    m_address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'markets'

class Restaurants(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    r_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    city_name = models.ForeignKey(City, models.DO_NOTHING, db_column='city_name')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    avg_rating = models.FloatField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    r_address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price_level = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurants'

    def __str__(self):
        return self.r_name

    def get_absolute_url(self):
        return reverse("travel:restaurants-detail", kwargs={"my_id": self.restaurant_id})