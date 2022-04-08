from turtle import title
from django import forms
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
from comment.models import (
    delete_comment_by_id,
    get_all_comment,
    AccommodationsComments,
    AttractionsComments,
    RestaurantsComments
)
from accounts.models import (
    Users,
    Preference
)

class CommentForm(forms.Form):

    comment_date = forms.DateField (widget=forms.TextInput(attrs={"placeholder": "Write your comment_date"}))
    comment = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write your comment"}))
    rating_score = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "rating from 1 to 5 points"}))
    
    #with connection.cursor() as cursor:
    #         cursor.execute("INSERT INTO restauratns_comments(comment_id, user_id, restaurant_id,comment_date,comment,comment_likes) VALUES (%s,%s,%s)",
    #         [comment_id, user_id, restaurant_id,comment_date,comment,rating])
