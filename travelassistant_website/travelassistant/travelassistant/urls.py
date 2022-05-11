"""travelassistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from django.conf import settings #add this
from . import views
from django.conf.urls.static import static #add this

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# from trip.views import test, search_restaurants

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^$',views.HomePage.as_view(), name='home'),
    # re_path(r'^comment/', include('comment.urls', namespace='comment')),
    re_path(r'^comment/', include('comment.urls', namespace='comment')),
    re_path(r'^accounts/', include('accounts.urls', namespace='accounts')),
    re_path(r'^trip/', include('trip.urls', namespace='trip')),
    # re_path(r'^trip/$', views.TripPage, name='trip'),
    # re_path(r'^thanks/$', views.ThankPage.as_view(), name='thanks'),
    # path(r'test', test),
    # url(r'trip', search_restaurants, name='search_restaurants'),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()