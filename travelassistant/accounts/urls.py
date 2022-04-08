from django.urls import include, re_path
from django.urls.conf import path, include
from django.conf import settings #add this
from django.conf.urls.static import static  # new
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'


# urlpatterns = [
#     url(r'login/$',auth_views.LoginView.as_view(template_name='accounts/login.html'),
#                     name='login'),
#     url(r'logout/$',auth_views.LogoutView.as_view(), name='logout'),
#     url(r'signup/$',views.SignUp.as_view(), name='signup')

# ]
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('account_actions/', views.account_actions_view, name='account_actions'),
    path('account_actions/delete_account/', views.delete_account_view, name='delete_account'),
    path('account_actions/update_account/', views.update_account_view, name='update_account'),
    # path('captcha/', include('captcha.urls')),
]
