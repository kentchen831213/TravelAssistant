from turtle import title
from unittest import result
from django import forms
from django.db import connections
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

class MainPageForm(forms.Form):
    city = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Your city", "class":"form-select"}))

    def clean_city(self, *args, **kwargs):
        city = self.cleaned_data.get("city")
        ls = city_list()
        if city not in ls:
            raise forms.ValidationError("This is not a valid city")
        return city
    def clean_spot(self, *args, **kwargs):
        spot = self.cleaned_data.get("spot")
        ls = ['restaurants', 'attractions', 'accommodations']
        if spot not in ls:
            raise forms.ValidationError("This is not a valid input")
        return spot

class TripSearchBoxForm(forms.Form):
    city_ls = city_list()
    city_ls = [('Select a City','Select a City')] + list_to_options(city_ls)
    spot_ls = [('Select a Category','Select a Category')] + list_to_options(['Restaurants', 'Attractions', 'Accommodations'])

    city = forms.ChoiceField(label='City', choices=city_ls, widget=forms.Select(attrs={'class':'form-select form-select-lg mb-3'}))
    spot = forms.ChoiceField(label='What to Search', choices=spot_ls, widget=forms.Select(attrs={'class':'form-select form-select-lg mb-3'}))
    keyword = forms.CharField(label="Search", max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control', "class":"form-control"}))

    def clean_city(self):
        city = self.cleaned_data.get("city")
        if city == 'Select a City':
            raise forms.ValidationError("Please Select a City!")
        return city

    def clean_spot(self):
        spot = self.cleaned_data.get("spot")
        if spot == 'Select a Category':
            raise forms.ValidationError("Please Select Restaurants, Attractions, or Accommodations!")
        return spot

class AdvancedSearchForm(forms.Form):
    city_ls = city_list()
    city_ls = [('Select a City','Select a City')] + list_to_options(city_ls)

    city = forms.ChoiceField(label='City', choices=city_ls, widget=forms.Select(attrs={'class':'form-select form-select-lg mb-3'}))
    # spot = forms.ChoiceField(label='What to Search', choices=spot_ls)

    # attraction_category = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Where do you want to go"}))
    attraction_category = forms.CharField(required = False, help_text="Keywords for attractions categories, e.g. museum.", label="Where do you want to go?", max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    restaurant_category = forms.CharField(required = False, help_text="Keywords for resstaurants categories, e.g. japanese.", label="What do you want to eat?", max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    accommodations_keyword = forms.CharField(required = False, help_text="Keywords for where you live.", label="Where you live?", max_length=255,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    # restaurant_category = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "What do you want to eat"}))

    def clean_city(self):
        city = self.cleaned_data.get("city")
        if city == 'Select a City':
            raise forms.ValidationError("Please Select a City!")
        return city

    # def clean_spot(self):
    #     spot = self.cleaned_data.get("spot")
    #     if spot == '':
    #         raise forms.ValidationError("Please Select Restaurants, Attractions, or Accommodations!")
    #     return spot
