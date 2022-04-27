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


def city_list():
    # with connections['travel_db'].cursor() as cursor:
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT city_name FROM city")
        c = [item[0] for item in cursor.fetchall()]
    return c

def list_to_options(city_ls):
    choices = []
    for x in city_ls:
        choices = choices + [(x, x)]
    return choices

class CommentForm(forms.Form):

    comment_date = forms.DateField (widget=forms.TextInput(attrs={"placeholder": "Write your comment_date"}))
    comment = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Write your comment"}))
    rating_score = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": "rating from 1 to 5 points"}))


class CommentBoxSearchForm(forms.Form):

    spot_ls = [('Select a Category','Select a Category')] + list_to_options(['Restaurants', 'Attractions', 'Accommodations'])

    spot = forms.ChoiceField(label='What to Search', choices=spot_ls)
    keyword = forms.CharField(label="Search", max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))


    def clean_spot(self):
        spot = self.cleaned_data.get("spot")
        if spot == 'Select a Category':
            raise forms.ValidationError("Please Select Restaurants, Attractions, or Accommodations!")
        return spot

    #with connection.cursor() as cursor:
    #         cursor.execute("INSERT INTO restauratns_comments(comment_id, user_id, restaurant_id,comment_date,comment,comment_likes) VALUES (%s,%s,%s)",
    #         [comment_id, user_id, restaurant_id,comment_date,comment,rating])
