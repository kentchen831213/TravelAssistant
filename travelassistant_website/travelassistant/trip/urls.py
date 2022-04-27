from django.urls import include, re_path
from django.urls.conf import path, include
from django.urls import include
from . import views

app_name = 'trip'
urlpatterns = [
    #url(r'trip_base/$',views.CreateRestaurants.as_view(),name='restaurant'),
    # url(r'trip_base/$', include('trip.urls', namespace='trip')),
    # url(r'^trip_base/$', views.TripPage.as_view(), name='trip_base'),
    path('', views.trip_search_view, name='trip_home'),
    path('trip_search_result/', views.trip_search_view, name='trip-search-result'),
    path('restaurants/<int:restaurant_id>/', views.restaurants_detail_view, name='restaurants-detail'),
    path('accommodations/<int:accommodation_id>/', views.accommodations_detail_view, name='accommodations-detail'),
    path('advanced_accommodations/<int:accommodation_id>/', views.advanced_accommodations_detail_view, name='advanced-accommodations-detail'),
    # path('advanced_accommodations/<int:accommodation_id>/<int:attraction_category>/<int:restaurant_category>', views.advanced_accommodations_detail_view, name='advanced-accommodations-detail'),
    path('attractions/<int:attraction_id>/', views.attractions_detail_view, name='attractions-detail'),
    # path('trip_search_result/', views.advanced_search_view, name='advanced-search'),
]
