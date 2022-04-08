from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from django.http import Http404 #handle missing object
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

#
# def insert_restaurant_comment(request):
#     form = CommentForm()
#     if request.metjod == 'POST':
#         form = CommentForm()
#         if form.is_valid():
#             comment = form.cleaned_data['message']
#             with connection.cursor() as cursor:
#                     cursor.execute("INSERT INTO restauratns_comments(u_name, password, email) VALUES (%s,%s,%s)",[username, password1, email])
#             return render(request,'restaurant_comment.html',comment)
#         else:
#             print(form.errors)

# def comment_base(request):
#     form=MainPageForm()
#     if request.method == "POST":
#         form = MainPageForm(request.POST)
#         if form.is_valid():
#             spots = spot_list(form.cleaned_data['spot'], form.cleaned_data['city'])
#             if form.cleaned_data['spot'] == 'restaurants' or form.cleaned_data['spot'] == 'accommodations':
#                 i = [ {'id': item[0], 'name': item[1], 'type': form.cleaned_data['spot']} for item in spots ]
#             elif form.cleaned_data['spot'] == 'attractions':
#                 i = [ {'id': item[0], 'name': item[3], 'type': form.cleaned_data['spot']} for item in spots ]
#             context = {
#                 'form': form,
#                 'spots': i,
#             }
#             return render(request, 'comment_base.html', context)
#         else:
#             print(form.errors)

#     context = {
#         'form': form
#     }
#     return render(request, 'comment_base.html', context)


def comment_detail(request):
    user_id = request.session['user_id']
    restaurant_comment_list = get_all_comment('restaurants_comments', user_id)
    restaurant_comment_result = [ {'restaurant_id':item[0],'comment_id': item[1], 'user_id': item[2], 'date':item[3],'comment':item[5],'r_name':item[7], 'like':item[6]} for item in restaurant_comment_list]
    attractions_comment_list = get_all_comment('attractions_comments', user_id)
    attractions_comment_result = [ {'attraction_id':item[0],'comment_id': item[1], 'user_id': item[2], 'date':item[3],'comment':item[5],'a_name':item[7], 'like':item[6]} for item in attractions_comment_list]
    accommodations_comment_list = get_all_comment('accommodations_comments', user_id)
    accommodations_comment_result = [ {'accommodation_id':item[0],'comment_id': item[1], 'user_id': item[2], 'date':item[3],'comment':item[5],'ac_name':item[7], 'like':item[6]} for item in accommodations_comment_list]
    context = {
        'restaurant_comment_result': restaurant_comment_result,
        'attractions_comment_result': attractions_comment_result,
        'accommodations_comment_result': accommodations_comment_result,
        'user_id': user_id,
    }
    return render(request, 'comment_detail.html', context)

def comment_delete(request, comment_id):
    if request.method == "POST":
        user_id = request.session['user_id']

        if request.POST['submit'] == "Delete Restaurants Comment":
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM restaurants_comments WHERE comment_id=%s",[comment_id])
        elif request.POST['submit'] == "Delete Accommodations Comment":
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM accommodations_comments WHERE comment_id=%s",[comment_id])
        elif request.POST['submit'] == "Delete Attractions Comment":
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM attractions_comments WHERE comment_id=%s",[comment_id])

        restaurant_comment_list = get_all_comment('restaurants_comments', user_id)
        restaurant_comment_result = [ {'restaurant_id':item[0],'comment_id': item[1], 'user_id': item[2], 'date':item[3],'comment':item[5],'r_name':item[7], 'like':item[6]} for item in restaurant_comment_list]
        attractions_comment_list = get_all_comment('attractions_comments', user_id)
        attractions_comment_result = [ {'attraction_id':item[0],'comment_id': item[1], 'user_id': item[2], 'date':item[3],'comment':item[5],'a_name':item[7], 'like':item[6]} for item in attractions_comment_list]
        accommodations_comment_list = get_all_comment('accommodations_comments', user_id)
        accommodations_comment_result = [ {'accommodation_id':item[0],'comment_id': item[1], 'user_id': item[2], 'date':item[3],'comment':item[5],'ac_name':item[7], 'like':item[6]} for item in accommodations_comment_list]
        context = {
            'restaurant_comment_result': restaurant_comment_result,
            'attractions_comment_result': attractions_comment_result,
            'accommodations_comment_result': accommodations_comment_result,
            'user_id': user_id,
        }
        return render(request, 'comment_detail.html', context)

def comment_edit(request, comment_id):

    if request.method == "POST":
        user_id = request.session['user_id']
        if request.POST['submit'] == "Edit Restaurants Comment":
            with connection.cursor() as cursor:
                query = "SELECT * FROM restaurants_comments WHERE comment_id = {};".format(comment_id)
                cursor.execute(query)
                r_comment = cursor.fetchall()[0]
            
            obj = Restaurants.objects.get(restaurant_id=r_comment[2])
            initial_value = {'comment': r_comment[5],
                    # 'comment_date':r_comment[3],
                    'rating_score': r_comment[4]
            }
            edit_type = 'restaurants_comments'

        elif request.POST['submit'] == "Edit Accommodations Comment":
            with connection.cursor() as cursor:
                query = "SELECT * FROM accommodations_comments WHERE comment_id = {};".format(comment_id)
                cursor.execute(query)
                r_comment = cursor.fetchall()[0]
            
            obj = Accommodations.objects.get(accommodation_id=r_comment[2])
            initial_value = {'comment': r_comment[5],
                    # 'comment_date':r_comment[3],
                    'rating_score': r_comment[4]
            }
            edit_type = 'accommodations_comments'


        elif request.POST['submit'] == "Edit Attractions Comment":
            with connection.cursor() as cursor:
                query = "SELECT * FROM attractions_comments WHERE comment_id = {};".format(comment_id)
                cursor.execute(query)
                r_comment = cursor.fetchall()[0]
            
            obj = Attractions.objects.get(attraction_id=r_comment[2])
            initial_value = {'comment': r_comment[5],
                    # 'comment_date':r_comment[3],
                    'rating_score': r_comment[4]
            }
            edit_type = 'attractions_comments'


        target_form = CommentForm(initial=initial_value)
        # target_form = CommentForm()
        context = {
            'comment_id': comment_id,
            'edit_type': edit_type,
            'comment_form': target_form,
            # 'r_comment': r_comment[3],
            'object': obj
        }
        return render(request, 'comment_edit.html', context)
    
    comment_form = CommentForm()
    context = {
        'comment_form': comment_form
    }
    return render(request, 'comment_edit.html', context)

def comment_update(request, comment_id):
    
    if request.method == "POST":
        if request.POST['comment_button'] == "Update Restaurants Comment":
            update_form = CommentForm(request.POST)
            if update_form.is_valid():
                input_comment_date = update_form.cleaned_data['comment_date']
                input_comment = update_form.cleaned_data['comment']
                input_comment_rating = update_form.cleaned_data['rating_score']
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE restaurants_comments SET comment_date = '{}', comment = '{}', rating = {} WHERE comment_id = '{}';".format(
                        input_comment_date, input_comment, input_comment_rating, comment_id))
        
        elif request.POST['comment_button'] == "Update Accommodations Comment":
            update_form = CommentForm(request.POST)
            if update_form.is_valid():
                input_comment_date = update_form.cleaned_data['comment_date']
                input_comment = update_form.cleaned_data['comment']
                input_comment_rating = update_form.cleaned_data['rating_score']
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE accommodations_comments SET comment_date = '{}', comment = '{}', rating = {} WHERE comment_id = '{}';".format(
                        input_comment_date, input_comment, input_comment_rating, comment_id))
        
        elif request.POST['comment_button'] == "Update Attractions Comment":
            update_form = CommentForm(request.POST)
            if update_form.is_valid():
                input_comment_date = update_form.cleaned_data['comment_date']
                input_comment = update_form.cleaned_data['comment']
                input_comment_rating = update_form.cleaned_data['rating_score']
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE attractions_comments SET comment_date = '{}', comment = '{}', rating = {} WHERE comment_id = '{}';".format(
                        input_comment_date, input_comment, input_comment_rating, comment_id))
            
    form=CommentForm()
    return redirect('/comment/comment_detail')

