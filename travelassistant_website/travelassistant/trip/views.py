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
from .forms import TripSearchBoxForm, AdvancedSearchForm
from .models import City
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render

# Create your views here.
# from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic import TemplateView


class TripPage(TemplateView):
    template_name = 'trip.html'


# ------------------------------------
# Tessa Travel Search
# ------------------------------------


# def city_list(request):
#     context ={}
#     context["dataset"] = City.objects.raw("SELECT * FROM City WHERE area < 400")


def trip_search_view(request):
    if request.method == "POST":
        if request.POST['submit'] == "Search":
            form_result = TripSearchBoxForm(request.POST)
            if form_result.is_valid():
                query_result = spot_list(
                    form_result.cleaned_data['spot'], form_result.cleaned_data['city'], form_result.cleaned_data['keyword'])
                result_list = []
                if form_result.cleaned_data['spot'] == 'Restaurants' or form_result.cleaned_data['spot'] == 'Accommodations':
                    result_list = [{'id': item[0], 'name': item[1],
                                    'type': form_result.cleaned_data['spot']} for item in query_result]
                elif form_result.cleaned_data['spot'] == 'Attractions':
                    result_list = [{'id': item[0], 'name': item[3],
                                    'type': form_result.cleaned_data['spot']} for item in query_result]
                context = {
                    # 'trip_search_box_form': TripSearchBoxForm(),
                    'trip_search_box_form': form_result,
                    'advanced_search_form': AdvancedSearchForm(),
                    'form_result': form_result,
                    'result_list': result_list,
                }
                return render(request, 'trip/trip_search_result.html', context)
            else:
                print(form_result.errors)

        elif request.POST['submit'] == "Choose where you live in the city?":
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
                    # 'trip_search_box_form': TripSearchBoxForm(),
                    'advanced_search_form': form_result,
                    'form_result': form_result,
                    'result_list': result_list,
                    'attraction_category': attraction_category,
                    'restaurant_category': restaurant_category,
                }
            return render(request, 'trip/advanced_search_result.html', context)

    context = {
        'trip_search_box_form': TripSearchBoxForm(),
        'advanced_search_form': AdvancedSearchForm(),
    }
    return render(request, 'trip.html', context)


def spot_list(spot, city, keyword):
    # with connections['travel_db'].cursor() as cursor:
    with connections['default'].cursor() as cursor:
        if spot.lower() == 'restaurants':
            n = 'r_name'
        elif spot.lower() == 'accommodations':
            n = 'ac_name'
        elif spot.lower() == 'attractions':
            n = 'a_name'
        query = "SELECT * FROM {s} WHERE city_name = '{c}' AND {n} LIKE '%{k}%';".format(
            s=spot.lower(), c=city, n=n, k=keyword)
        cursor.execute(query)
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

            # with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO accommodations_comments(user_id, accommodation_id, comment_date, comment, rating) VALUES (%s,%s,%s,%s,%s)",
                [request.session['user_id'] , accommodation_id, comment_date, comment, rating])
                # writr update user to activate trigger
                query = """
                UPDATE users SET superstar = False WHERE user_id = '{}';
                """.format(request.session['user_id'])
                cursor.execute(query)
            return redirect('/comment/comment_detail')

    comment_form = CommentForm()
    context = {
        "object": obj,
        "comment_form": comment_form,
        "laundrymarket": result_list,
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

            # with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO attractions_comments(user_id, attraction_id, comment_date, comment, rating) VALUES (%s,%s,%s,%s,%s)",
                [request.session['user_id'] , attraction_id, comment_date, comment, rating])
                # writr update user to activate trigger
                query = """
                UPDATE users SET superstar = False WHERE user_id = '{}';
                """.format(request.session['user_id'])
                cursor.execute(query)
            return redirect('/comment/comment_detail')


    comment_form = CommentForm()
    context = {
        "object": obj,
        "comment_form": comment_form
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

            # with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO restaurants_comments(user_id, restaurant_id, comment_date, comment, rating) VALUES (%s,%s,%s,%s,%s)",
                [request.session['user_id'] , restaurant_id, comment_date, comment, rating])
                # writr update user to activate trigger
                query = """
                UPDATE users SET superstar = False WHERE user_id = '{}';
                """.format(request.session['user_id'])
                cursor.execute(query)
            return redirect('/comment/comment_detail')

    comment_form = CommentForm()
    context = {
        "object": obj,
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
    # with connections['travel_db'].cursor() as cursor:
    with connections['default'].cursor() as cursor:
        query = """
        SELECT * FROM (
        (SELECT ac_name, m_name as name, 'market' as type, SQRT(power((ac.latitude - m.latitude), 2) + power((ac.longitude - m.longitude), 2)) * 100 AS approximate_distance
        FROM markets m JOIN accommodations ac USING(city_name)
        WHERE SQRT(power((ac.latitude - m.latitude), 2) + power((ac.longitude - m.longitude), 2)) * 100 < 5
        AND m.latitude IS NOT NULL AND m.longitude IS NOT NULL AND ac_name = '{}')
        UNION
        (SELECT ac_name, l_name as name, 'laundry' as type, SQRT(power((ac.latitude - l.latitude), 2) + power((ac.longitude - l.longitude), 2)) * 100 AS approximate_distance
        FROM laundry l JOIN accommodations ac USING(city_name)
        WHERE SQRT(power((ac.latitude - l.latitude), 2) + power((ac.longitude - l.longitude), 2)) * 100 < 5 AND
        l.latitude IS NOT NULL AND l.longitude IS NOT NULL AND ac_name = '{}')) AS temp ORDER BY approximate_distance;
        """.format(name, name)
        cursor.execute(query)
        c = cursor.fetchall()
    return c

# ------------------------------------------------------------ #
# Functions for the second advanced query
# ------------------------------------------------------------ #
# def advanced_search_view(request):
#     if request.method == "POST":
#         form_result = AdvancedSearchForm(request.POST)
#         if form_result.is_valid():
#             spots = search_accomodation(form_result.cleaned_data['spot'], form_result.cleaned_data['city'],
#                                         form_result.cleaned_data['attraction_category'], form_result.cleaned_data['restaurant_category'])
#             i = [{'attraction': item[0], 'restaurant': item[1],
#                   'distance1': item[2], 'distance2': item[3]} for item in spots]
#             print(spots)
#             context = {
#                 'advanced_search_form': form_result,
#                 'spots': i,
#             }
#             return render(request, 'trip/search_attraction_restaurant.html', context)
#         else:
#             print(form_result.errors)

#     advanced_search_form = AdvancedSearchForm()
#     context = {
#         'advanced_search_form': advanced_search_form
#     }
#     return render(request, 'trip.html', context)

# def advanced_search_view(request):
#     if request.method == "POST":
#         form_result = AdvancedSearchForm(request.POST)
#         if form_result.is_valid():
#             query_result = spot_list(
#                 'accommodations', form_result.cleaned_data['city'], '')

#             attraction_category = form_result.cleaned_data['attraction_category']
#             restaurant_category = form_result.cleaned_data['restaurant_category']
#             result_list = [{'id': item[0], 'name': item[1],
#                                 'type': form_result.cleaned_data['spot']} for item in query_result]
#             advanced_search_form = AdvancedSearchForm()
#             context = {
#                 'trip_search_box_form': advanced_search_form,
#                 'form_result': form_result,
#                 'result_list': result_list,
#                 'attraction_category': attraction_category,
#                 'restaurant_category': restaurant_category,
#             }
#         return render(request, 'trip/trip_search_result.html', context)

#     advanced_search_form = AdvancedSearchForm()
#     context = {
#         'advanced_search_form': advanced_search_form
#     }
#     return render(request, 'trip.html', context)

# def advanced_accommodations_detail_view(request, accommodation_id, attraction_category, restaurant_category):
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
    # print(i)
    return render(request, 'trip/advanced_attractions_detail.html', context)


def search_accomodation(obj, attraction_category, restaurant_category):
    city = str(obj.city_name).replace('City object', '').replace(' ','').replace('(','').replace(')','')
    name = obj.ac_name
    # with connections['travel_db'].cursor() as cursor:
    with connections['default'].cursor() as cursor:
        query = """
        SELECT DISTINCT a.a_name, r.r_name,
            SQRT(power((ac.latitude - a.latitude), 2) + power((ac.longitude - a.longitude), 2)) * 100 AS ac_a_distance,
            SQRT(power((a.latitude - r.latitude), 2) + power((a.longitude - r.longitude), 2)) * 100 AS a_r_distance
        FROM attractions a JOIN accommodations ac USING (city_name) JOIN restaurants r USING (city_name)
        WHERE ac_name = '{n}' AND
            LOWER(a.categories) LIKE '%{a}%' AND
            SQRT(power((a.latitude - r.latitude), 2) + power((a.longitude - r.longitude), 2)) * 100 < 5 AND
            r.restaurant_id IN (SELECT r.restaurant_id
                         FROM restaurants_comments rm JOIN restaurants r ON r.restaurant_id = rm.restaurant_id
                         WHERE r.city_name = '{c}' AND r.category LIKE '%{r}%'
                         GROUP BY rm.restaurant_id
                         HAVING COUNT(rm.restaurant_id) > 0)
        ORDER BY ac_a_distance, r.r_name DESC;
        """.format(c=city, n=name, a=attraction_category.lower(), r=restaurant_category.lower())
        cursor.execute(query)
        c = cursor.fetchall()
    return c
