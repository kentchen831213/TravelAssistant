from django.db import models
from django.urls import reverse
from django.db import connections
from django.db import connection

from trip.models import (
    Accommodations,
    Attractions,
    City,
    Laundry,
    Markets,
    Restaurants,
)

from accounts.models import (
    Users,
    Preference
)

# def search_all_comment(db_name, user_id):
#     with connections['default'].cursor() as cursor:
#         query = "SELECT * FROM {db} WHERE user_id = '{u}';".format(db=db_name, u=user_id)
#         cursor.execute(query)
#         c = cursor.fetchall()
#     return c

def get_all_comment(db_name, user_id):
    with connections['default'].cursor() as cursor:
        if db_name == 'restaurants_comments':
            query = "SELECT * FROM restaurants_comments JOIN restaurants USING(restaurant_id) where user_id = '{}';".format(user_id)

        elif db_name == 'attractions_comments':
            query = "SELECT * FROM attractions_comments JOIN attractions USING(attraction_id) where user_id = '{}';".format(user_id)

        elif db_name == 'accommodations_comments':
            query = "SELECT * FROM accommodations_comments JOIN accommodations USING(accommodation_id) where user_id = '{}';".format(user_id)

        cursor.execute(query)
        c = cursor.fetchall()
    return c

def delete_comment_by_id(db_name, comment_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM {db} WHERE comment_id={id}".format(db=db_name, id=comment_id))


class AttractionsComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255)
    attraction_id = models.ForeignKey(Attractions, models.DO_NOTHING)
    comment_date = models.DateField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    comment_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attractions_comments'
        unique_together = (('comment_id', 'user_id', 'attraction_id'),)

class AccommodationsComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING)
    accommodation_id = models.ForeignKey(Accommodations, models.DO_NOTHING)
    comment_date = models.DateField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    comment_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accommodations_comments'
        unique_together = (('comment_id', 'user_id', 'accommodation_id'),)

class RestaurantsComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, models.DO_NOTHING)
    restaurant_id = models.ForeignKey(Restaurants, models.DO_NOTHING)
    comment_date = models.DateField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    comment_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurants_comments'
        unique_together = (('comment_id', 'user_id', 'restaurant_id'),)