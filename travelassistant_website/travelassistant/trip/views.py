import os

from numpy import character
from travelassistant.settings import BASE_DIR
from sys import implementation
from django.http import Http404  # handle missing object
from trip.models import (
    Accommodations,
    Attractions,
    City,
    Laundry,
    Markets,
    Restaurants,
)
from comment.models import (
    AccommodationsComments,
    AttractionsComments,
    RestaurantsComments
)
from comment.forms import (
    CommentForm
)
from accounts.models import (
    Users,
    Preference,
)
from django.db import connections, connection
from .forms import TripSearchBoxForm, AdvancedSearchForm, MainPageForm, city_list
from .models import City
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import TemplateView

class TripPage(TemplateView):
    template_name = 'trip.html'

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

current_path = os.getcwd()

# ------------------------------------------------------------ #
# Bsic Search - Search Box 1
# ------------------------------------------------------------ #
def get_image_path(spot_type, spot_id):
    """
    Check if a image exists, if not return the default image.
    """
    image_path = str("{}/".format(spot_type)+str(spot_id)+".jpg")
    if not os.path.exists(os.path.join(BASE_DIR, "static/", image_path)):
        image_path = str("{}/default.jpg".format(spot_type))

    return image_path

def trip_search_view(request):
    request.GET.get('page', 1)

    if request.method == "POST":
        if request.POST['submit'] == "Search":
            form_result = TripSearchBoxForm(request.POST)
            if form_result.is_valid():
                query_result = spot_list(
                    form_result.cleaned_data['spot'], form_result.cleaned_data['city'], form_result.cleaned_data['keyword'])
                result_list = []
                if form_result.cleaned_data['spot'] == 'Restaurants':
                    result_list = [{'id': item[0], 'name': item[1], 'image': get_image_path('restaurants', item[0]),
                                    'type': form_result.cleaned_data['spot']} for item in query_result]
                elif form_result.cleaned_data['spot'] == 'Accommodations':
                    result_list = [{'id': item[0], 'name': item[1], 'image': get_image_path('accommodations', item[0]),
                                    'type': form_result.cleaned_data['spot']} for item in query_result]
                elif form_result.cleaned_data['spot'] == 'Attractions':
                    result_list = [{'id': item[0], 'name': item[3], 'image': get_image_path('attractions', item[0]),
                                    'type': form_result.cleaned_data['spot']} for item in query_result]

                paginator = Paginator(result_list, 10)
                page_number=request.GET.get('page', 1)

                try:
                    page_obj = paginator.get_page(page_number)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)

                context = {
                    'trip_search_box_form': TripSearchBoxForm(),
                    'advanced_search_form': AdvancedSearchForm(),
                    'form_result': form_result,
                    'result_list': page_obj,
                }
                return render(request, 'trip/trip_search_result.html', context)
            else:
                print(form_result.errors)

        elif request.POST['submit'] == "Choose where you live in the city":

            form_result = AdvancedSearchForm(request.POST)
            if form_result.is_valid():
                attraction_category = form_result.cleaned_data['attraction_category']
                restaurant_category = form_result.cleaned_data['restaurant_category']
                accommodations_keyword = form_result.cleaned_data['accommodations_keyword']
                query_result = spot_list(
                    'accommodations', form_result.cleaned_data['city'], accommodations_keyword)

                result_list = [{'id': item[0], 'name': item[1],
                                    'type': 'accommodations'} for item in query_result]
                request.session['attraction_category'] = attraction_category
                request.session['restaurant_category'] = restaurant_category
                context = {
                    'advanced_search_form': form_result,
                    'form_result': form_result,
                    'result_list': result_list,
                    'attraction_category': attraction_category,
                    'restaurant_category': restaurant_category,
                    'trip_search_box_form': TripSearchBoxForm(),
                    'advanced_search_form': AdvancedSearchForm(),
                }
                return render(request, 'trip/advanced_search_result.html', context)
            else:
                print(form_result.errors)

    context = {
        'trip_search_box_form': TripSearchBoxForm(),
        'advanced_search_form': AdvancedSearchForm(),
    }
    return render(request, 'trip.html', context)

# ------------------------------------------------------------ #
# Applied for Procedures: Package Search View
# ------------------------------------------------------------ #
def package_search_view(request):
    # try:
        varAccommodationMaxPrice = 0
        varAccommodationMinPrice = 0
        varAccommodationMinBeds = 0
        varAccommodationMaxBeds = 0
        varAccommodationMinBedroom = 0
        varAccommodationMaxBedroom = 0
        varRestaurantMinRating = 0
        varRestaurantMaxRating = 5

        # deal with accommodations
        if request.GET['hotel_price'] == "Less than $50":
            varAccommodationMaxPrice = 50
        elif request.GET['hotel_price'] == "$50-$100":
            varAccommodationMaxPrice = 100
            varAccommodationMinPrice = 50
        elif request.GET['hotel_price'] == "$100-$150":
            varAccommodationMaxPrice = 150
            varAccommodationMinPrice = 100
        elif request.GET['hotel_price'] == "$150-$200":
            varAccommodationMaxPrice = 200
            varAccommodationMinPrice = 150
        elif request.GET['hotel_price'] == "More than $200":
            varAccommodationMaxPrice = 100000000000
            varAccommodationMinPrice = 200

        if request.GET['people_count'] == "1":
            varAccommodationMaxBeds = 1
        elif request.GET['people_count'] == "2":
            varAccommodationMaxBeds = 2
            varAccommodationMinBeds = 2
        elif request.GET['people_count'] == "3-4":
            varAccommodationMaxBeds = 4
            varAccommodationMinBeds = 3
        elif request.GET['people_count'] == "5-10":
            varAccommodationMaxBeds = 10
            varAccommodationMinBeds = 5
        elif request.GET['people_count'] == "More than 10":
            varAccommodationMaxBeds = 1000
            varAccommodationMinBeds = 10


        if request.GET['rooms_count'] == "1":
            varAccommodationMaxBedroom = 1
        elif request.GET['rooms_count'] == "2":
            varAccommodationMaxBedroom = 2
            varAccommodationMinBedroom = 2
        elif request.GET['rooms_count'] == "3-4":
            varAccommodationMaxBedroom = 4
            varAccommodationMinBedroom = 3
        elif request.GET['rooms_count'] == "More than 5 rooms":
            varAccommodationMaxBedroom = 1000
            varAccommodationMinBedroom = 5

        if request.GET['rating'] == "1":
            varRestaurantMinRating = 1
        elif request.GET['rating'] == "2":
            varRestaurantMinRating = 2
        elif request.GET['rating'] == "3":
            varRestaurantMinRating = 3
        elif request.GET['rating'] == "4":
            varRestaurantMinRating = 4
        elif request.GET['rating'] == "5":
            varRestaurantMinRating = 5

        attraction_keyword_1 = '%{}%'.format(str(request.GET['attractions_type1']).lower())
        attraction_keyword_2 = '%{}%'.format(str(request.GET['attractions_type2']).lower())
        attraction_keyword_3 = '%{}%'.format(str(request.GET['attractions_type3']).lower())

        with connections['default'].cursor() as cursor:
            cursor.execute("CALL PackageSearch(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    [request.session['user_id'], request.GET['city'],
                    attraction_keyword_1, attraction_keyword_2, attraction_keyword_3,
                    varAccommodationMaxPrice, varAccommodationMinPrice, varAccommodationMinBeds, varAccommodationMaxBeds,
                    varAccommodationMinBedroom, varAccommodationMaxBedroom, request.GET['restaurant_price_level'],request.GET['restaurant_types'], varRestaurantMinRating, varRestaurantMaxRating ])
            cursor.execute("SELECT * FROM PreferenceTable;")
            query_result = cursor.fetchall()

        preference_result_list = [{'preference_id': item[0], 'user_id': item[1],
                            'spot_type': item[2], 'spot_id': item[3], 'spot_name': item[4]} for item in query_result]

        # Query to get more detail information by id
        # Attractions
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT * FROM (SELECT * FROM PreferenceTable where spot_type = 'attractions') AS p1 JOIN attractions a ON p1.spot_id = a.attraction_id ORDER BY a.ranking LIMIT 0, 5;")
            query_result = cursor.fetchall()

        attraction_result_list = [{'preference_id': item[0], 'user_id': item[1],
                            'spot_type': str(item[2]).capitalize(), 'spot_id': item[3], 'spot_name': item[4], 'ranking':item[6],
                            'category': str(item[9]).capitalize(),  'address':item[10], 'latitude':item[11], 'longitude':item[12], 'image': get_image_path('attractions', item[3])} for item in query_result]

        # Restaurants
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT * FROM (SELECT * FROM PreferenceTable where spot_type = 'restaurants') AS p1 JOIN restaurants r ON p1.spot_id = r.restaurant_id ORDER BY r.avg_rating DESC LIMIT 0, 5;")
            query_result = cursor.fetchall()

        restaurant_result_list = [{'preference_id': item[0], 'user_id': item[1],
                            'spot_type': str(item[2]).capitalize(), 'spot_id': item[3], 'spot_name': item[4], 'avg_rating': item[11], 'description':item[14],
                            'category': str(item[7]).capitalize(),  'address':item[13], 'latitude':item[9], 'longitude':item[10], 'image': get_image_path('restaurants', item[3])} for item in query_result]

        # Accommodations
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT * FROM (SELECT * FROM PreferenceTable where spot_type = 'accommodations') AS p1 JOIN accommodations ac ON p1.spot_id = ac.accommodation_id ORDER BY ac.avg_rating DESC LIMIT 0, 3;")
            query_result = cursor.fetchall()

        accommodation_result_list = [{'preference_id': item[0], 'user_id': item[1],
                            'spot_type': str(item[2]).capitalize(), 'spot_id': item[3], 'spot_name': item[4],
                            'county': str(item[7]).capitalize(),
                            'avg_rating': item[11], 'price_level':item[12], 'latitude':item[9], 'longitude':item[10],
                            'bathrooms': item[14], 'bedrooms': item[15], 'beds': item[16],
                            'image': get_image_path('accommodations', item[3])} for item in query_result]



        context = {
            'trip_search_box_form': TripSearchBoxForm(),
            'advanced_search_form': AdvancedSearchForm(),
            'preference_result_list': preference_result_list,
            'attraction_result_list': attraction_result_list,
            'restaurant_result_list': restaurant_result_list,
            'accommodation_result_list': accommodation_result_list

        }
        return render(request, 'trip/package_search_result.html', context)
    # except:
    #     context = {
    #         'trip_search_box_form': TripSearchBoxForm(),
    #         'advanced_search_form': AdvancedSearchForm(),
    #     }
    #     return render(request, 'trip.html', context)

# ------------------------------------------------------------ #
# Function: spot_list - query the database
# ------------------------------------------------------------ #
def spot_list(spot, city, keyword):
    # with connections['default'].cursor() as cursor:
    with connections['default'].cursor() as cursor:
        if spot.lower() == 'restaurants':
            cursor.execute("SELECT * FROM restaurants WHERE city_name = '%s' AND r_name LIKE '%%%s%%';"
                % (city, keyword))

        elif spot.lower() == 'accommodations':
            cursor.execute("SELECT * FROM accommodations WHERE city_name = '%s' AND ac_name LIKE '%%%s%%';"
                % (city, keyword))

        elif spot.lower() == 'attractions':
            cursor.execute("SELECT * FROM attractions WHERE city_name = '%s' AND a_name LIKE '%%%s%%';"
                % (city, keyword))
        c = cursor.fetchall()
    return c

# ------------------------------------------------------------ #
# Details pages view
# ------------------------------------------------------------ #
def accommodations_detail_view(request, accommodation_id):
    # try:
    obj = Accommodations.objects.get(accommodation_id=accommodation_id)
    laundrymarket = neighborhood(obj.ac_name)
    result_list = [{'name': item[1], 'type': item[2], 'distance': item[3]}
            for item in laundrymarket]
    # except:
    #     raise Http404

    if request.method == "POST":
        form_result = CommentForm(request.POST)
        if form_result.is_valid():
            comment_date = form_result.cleaned_data['comment_date']
            comment = form_result.cleaned_data['comment']
            rating = form_result.cleaned_data['rating_score']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO accommodations_comments(user_id, accommodation_id, comment_date, comment, rating) VALUES (%s,%s,%s,%s,%s)",
                    [request.session['user_id'] , accommodation_id, comment_date, comment, rating])
                # update user to activate trigger
                cursor.execute("""
                UPDATE users SET superstar = False WHERE user_id = %s;
                """, [request.session['user_id']])
            return redirect('/comment/comment_detail')

    comment_form = CommentForm()
    context = {
        "object": obj,
        "comment_form": comment_form,
        "laundrymarket": result_list,
        "image": get_image_path('accommodations', obj.accommodation_id),
    }
    return render(request, 'trip/accommodations_detail.html', context)

def attractions_detail_view(request, attraction_id):
    # try:
    obj = Attractions.objects.get(attraction_id=attraction_id)
    # except:
    #     raise Http404

    if request.method == "POST":
        form_result = CommentForm(request.POST)
        if form_result.is_valid():
            comment_date = form_result.cleaned_data['comment_date']
            comment = form_result.cleaned_data['comment']
            rating = form_result.cleaned_data['rating_score']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO attractions_comments(user_id, attraction_id, comment_date, comment, rating) VALUES (%s,%s,%s,%s,%s)",
                    [request.session['user_id'] , attraction_id, comment_date, comment, rating])
                cursor.execute("""
                UPDATE users SET superstar = False WHERE user_id = %s;
                """, [request.session['user_id']])
            return redirect('/comment/comment_detail')

    comment_form = CommentForm()
    context = {
        "object": obj,
        "comment_form": comment_form,
        "image": get_image_path('attractions', obj.attraction_id),
    }
    return render(request, 'trip/attractions_detail.html', context)

def restaurants_detail_view(request, restaurant_id):
    try:
        obj = Restaurants.objects.get(restaurant_id=restaurant_id)
    except:
        raise Http404

    # deal with the comment form
    if request.method == "POST":
        form_result = CommentForm(request.POST)
        if form_result.is_valid():
            comment_date = form_result.cleaned_data['comment_date']
            comment = form_result.cleaned_data['comment']
            rating = form_result.cleaned_data['rating_score']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO restaurants_comments(user_id, restaurant_id, comment_date, comment, rating) VALUES (%s,%s,%s,%s,%s)",
                    [request.session['user_id'] , restaurant_id, comment_date, comment, rating])
                # writr update user to activate trigger
                cursor.execute("""
                UPDATE users SET superstar = False WHERE user_id = %s;
                """, [request.session['user_id']])
            return redirect('/comment/comment_detail')

    comment_form = CommentForm()
    context = {
        "object": obj,
        "image": get_image_path('restaurants', obj.restaurant_id),
        "comment_form": comment_form
    }
    return render(request, 'trip/restaurants_detail.html', context)

# ------------------------------------------------------------ #
# Functions for the first advanced query
# ------------------------------------------------------------ #
def neighborhood(name):
    """
    The function will return all markets and laundries in the neighborhood of an accommodation.
    """
    # with connections['default'].cursor() as cursor:
    with connections['default'].cursor() as cursor:
        query = """
        SELECT * FROM (
        (SELECT ac_name, m_name as name, 'market' as type, SQRT(power((ac.latitude - m.latitude), 2) + power((ac.longitude - m.longitude), 2)) * 100 AS approximate_distance
        FROM markets m JOIN accommodations ac USING(city_name)
        WHERE SQRT(power((ac.latitude - m.latitude), 2) + power((ac.longitude - m.longitude), 2)) * 100 < 5
        AND m.latitude IS NOT NULL AND m.longitude IS NOT NULL AND ac_name = '%s')
        UNION
        (SELECT ac_name, l_name as name, 'laundry' as type, SQRT(power((ac.latitude - l.latitude), 2) + power((ac.longitude - l.longitude), 2)) * 100 AS approximate_distance
        FROM laundry l JOIN accommodations ac USING(city_name)
        WHERE SQRT(power((ac.latitude - l.latitude), 2) + power((ac.longitude - l.longitude), 2)) * 100 < 5 AND
        l.latitude IS NOT NULL AND l.longitude IS NOT NULL AND ac_name = '%s')) AS temp ORDER BY approximate_distance;
        """ % (name, name)
        cursor.execute(query)
        c = cursor.fetchall()
    return c

# ------------------------------------------------------------ #
# Functions for the second advanced query
# ------------------------------------------------------------ #
def advanced_accommodations_detail_view(request, accommodation_id):

        attraction_category = request.session['attraction_category']
        restaurant_category = request.session['restaurant_category']
        # try:
        obj = Accommodations.objects.get(accommodation_id=accommodation_id)
        # query_result = search_accomodation(obj, request.session['attraction_category'], request.session['restaurant_category'])
        query_result = search_accomodation(obj, attraction_category, restaurant_category)
        tourtist_list = [{'a_name': item[0], 'r_name': item[1], 'ac_a_distance': item[2], 'a_r_distance': item[3]}
                    for item in query_result]
        # except:
        #     raise Http404
        context = {
            "accommodation_id": accommodation_id,
            "attraction_category": attraction_category,
            "restaurant_category": restaurant_category,
            "object": obj,
            "tourtist_list": tourtist_list
        }
        return render(request, 'trip/advanced_attractions_detail.html', context)


def search_accomodation(obj, attraction_category, restaurant_category):
    city = str(obj.city_name).replace('City object', '').replace(' ','').replace('(','').replace(')','')
    name = obj.ac_name
    attraction_category = str(attraction_category).lower()
    restaurant_category = str(restaurant_category).lower()

    with connections['default'].cursor() as cursor:
        cursor.execute("""
        SELECT DISTINCT a.a_name, r.r_name,
            SQRT(power((ac.latitude - a.latitude), 2) + power((ac.longitude - a.longitude), 2)) * 100 AS ac_a_distance,
            SQRT(power((a.latitude - r.latitude), 2) + power((a.longitude - r.longitude), 2)) * 100 AS a_r_distance
        FROM attractions a JOIN accommodations ac USING (city_name) JOIN restaurants r USING (city_name)
        WHERE ac_name = '{}' AND
            LOWER(a.category) LIKE '%{}%' AND
            SQRT(power((a.latitude - r.latitude), 2) + power((a.longitude - r.longitude), 2)) * 100 < 5 AND
            r.restaurant_id IN (SELECT r.restaurant_id
                         FROM restaurants_comments rm JOIN restaurants r ON r.restaurant_id = rm.restaurant_id
                         WHERE r.city_name = '{}' AND r.category LIKE '%{}%'
                         GROUP BY rm.restaurant_id
                         HAVING COUNT(rm.restaurant_id) > 0)
        ORDER BY ac_a_distance, r.r_name DESC;
        """.format(name, attraction_category, city, restaurant_category))
        c = cursor.fetchall()
        # print(c)
    return c




# ------------------------------------------------------------ #
# New Add?
# ------------------------------------------------------------ #
def home_view(request):
    form=MainPageForm()
    city_ls = city_list()
    print(city_ls)
    if request.method == "POST":
        form = MainPageForm(request.POST)
        if form.is_valid():
            if request.POST.get("accommodation"):
                spot = 'accommodations'
                spots = spot_list2(spot, form.cleaned_data['city'])
                i = [ {'id': item[0], 'name': item[1], 'type': spot} for item in spots ]
            elif request.POST.get("attraction"):
                spot = 'attractions'
                spots = spot_list2(spot, form.cleaned_data['city'])
                i = [ {'id': item[0], 'name': item[3], 'type': spot} for item in spots ]
            elif request.POST.get("restaurant"):
                spot = 'restaurants'
                spots = spot_list2(spot, form.cleaned_data['city'])
                i = [ {'id': item[0], 'name': item[1], 'type': spot} for item in spots ]

            context = {
                'form': form,
                'spots': i,
                'city_ls': city_ls
            }
            return render(request, 'trip/home.html', context)
        else:
            print(form.errors)

    context = {
        'form': form,
        'city_ls': city_ls
    }
    return render(request, 'trip/home.html', context)


def spot_list2(spot, city):
    with connections['default'].cursor() as cursor:
        query = "SELECT * FROM {} WHERE city_name= \'{}\' ".format(spot, city)
        cursor.execute(query)
        c = cursor.fetchall()
    return c

def city_spot_view(request, my_id, my_id2):
    obj = spot_list2(my_id2, my_id)



    paginator = Paginator(obj, 10)
    page_number=request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    # try:
    #     obj = spot_list(my_id2, my_id)

    #     paginator = Paginator(obj, 5) # Show 25 contacts per page.
    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    # except:
    #     raise Http404
    context = {
        "object": page_obj,
        "my_id": my_id,
        "my_id2": my_id2
    }
    return render(request, 'trip/city_spot.html', context)

def advance_search_view(request):
    form_result = AdvancedSearchForm()
    if request.method == "POST":
        form_result = AdvancedSearchForm(request.POST)
        if form_result.is_valid():
            accommodations_keyword = form_result.cleaned_data['accommodations_keyword']
            query_result = spot_list2(
                'accommodations', form_result.cleaned_data['city'], accommodations_keyword)

            result_list = [{'id': item[0], 'name': item[1],
                                'type': 'accommodations'} for item in query_result]
            context = {
                'form_result': form_result,
                'result_list': result_list,
            }
            return render(request, 'travel/advance_search.html', context)
        else:
            print(form_result.errors)
    context = {
        'form_result': form_result,
    }
    return render(request, 'travel/advance_search.html', context)
