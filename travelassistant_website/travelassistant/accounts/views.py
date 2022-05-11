from django.shortcuts import render, redirect
from matplotlib.style import context
# from .models import Users, get_user_by_user_id, get_user_by_email, is_user_duplicate, create_new_user

from accounts.models import (
    Users,
    Preference
)

from trip.forms import TripSearchBoxForm, AdvancedSearchForm
from .forms import LogInForm, SignUpForm, PersonalpicForm
from django.db import connections
from django.views.generic import RedirectView
from django.http import Http404
from passlib.hash import pbkdf2_sha256


def login(request):
    """
    """
    if request.session.get('is_login', None):
        # The user is already signed in
        return render(request, 'index.html', locals())  # use the url name

    if request.method == "POST":
        login_form = LogInForm(request.POST)
        message = "Please check the content!"
        if login_form.is_valid():
            input_user_id = login_form.cleaned_data['user_id']
            input_password = login_form.cleaned_data['password']
            user = Users.get_user_by_user_id(input_user_id) # return a queryset
            if user:
                user = user[0]
                if user.verify_password(input_password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.user_id

                    context = {
                        'trip_search_box_form': TripSearchBoxForm(),
                        'advanced_search_form': AdvancedSearchForm(),
                    }
                    return render(request, 'index.html', context)
                else:
                    message = "Wrong Password!"
            else:
                message = "The UserID '{}' Does Not Exist!".format(input_user_id)
        return render(request, 'accounts/login.html', locals())

    login_form = LogInForm()
    return render(request, 'accounts/login.html', locals())


def signup(request):
    """
    Signup an user account
    """
    if request.session.get('is_login', None):
        # The user cannot create a new account when he/she is already signed in
        return render(request, 'index.html', locals())

    if request.method == "POST":
        signup_form = SignUpForm(request.POST, request.FILES)

        message = "Pleace check your input!"
        if signup_form.is_valid():
            input_user_id = signup_form.cleaned_data['user_id']
            input_password = signup_form.cleaned_data['password']
            input_password_validation = signup_form.cleaned_data['password_validation']
            input_first_name = signup_form.cleaned_data['first_name']
            input_last_name = signup_form.cleaned_data['last_name']
            input_gender = signup_form.cleaned_data['gender']
            input_email = signup_form.cleaned_data['email']
            input_phone = signup_form.cleaned_data['phone']
            input_city = signup_form.cleaned_data['city']
            input_birth_date = signup_form.cleaned_data['birth_date']
            # img = signup_form.cleaned_data.get("personal_pic")

            if input_password != input_password_validation:
                # password validation
                message = "Tow entered passwords are different!"
                return render(request, 'accounts/signup.html', locals())

            message, is_occupied = Users.is_user_duplicate(
                user_id=input_user_id, email=input_email)
            if is_occupied:
                return render(request, 'accounts/signup.html', locals())

            enc_password = pbkdf2_sha256.encrypt(input_password)

            Users.create_new_user(user_id=input_user_id, password=enc_password, first_name=input_first_name,
                                  last_name=input_last_name, gender=input_gender, email=input_email, phone=input_phone, city=input_city, birth_date=input_birth_date)

            return redirect("/accounts/login")

    signup_form = SignUpForm()
    return render(request, 'accounts/signup.html', locals())


def logout(request):
    """
    User logout
    """
    if not request.session.get('is_login', None):
        return render(request, 'index.html', locals())

    request.session.flush()
    return render(request, 'index.html', locals())


def account_actions_view(request):
    """
    Update Account or Delete the Account
    """
    # Generate the the original account result
    # try:
    user_id = request.session['user_id']
    user = Users.get_user_by_user_id(user_id=user_id)[0]
    # user = Users.get_user_by_user_id(user_id=user_id).first()
    # personalimage = PersonalpicForm(request.POST, request.FILES)

    context = {
        "user": user,
        # "userimage": personalimage
    }
    return render(request, 'accounts/account_actions.html', context)
    # except:
    #     raise Http404


def update_account_view(request):

    user = Users.get_user_by_user_id(request.session['user_id'])[0]
    # user = Users.get_user_by_user_id(request.session['user_id']).first()

    if request.method == "POST":
        update_form = SignUpForm(request.POST)
        message = "Pleace check your input!"
        if update_form.is_valid():
            input_user_id = update_form.cleaned_data['user_id']
            input_password = update_form.cleaned_data['password']
            input_password_validation = update_form.cleaned_data['password_validation']
            input_first_name = update_form.cleaned_data['first_name']
            input_last_name = update_form.cleaned_data['last_name']
            input_gender = update_form.cleaned_data['gender']
            input_email = update_form.cleaned_data['email']
            input_phone = update_form.cleaned_data['phone']
            input_city = update_form.cleaned_data['city']
            input_birth_date = update_form.cleaned_data['birth_date']

            if input_password != input_password_validation:
                # password validation
                message = "Tow entered passwords are different!"
                return render(request, "accounts/account_actions/update_account.html", locals())

            if input_email != user.email:
                message, is_occupied = Users.is_user_duplicate(
                    email=input_email)
                if is_occupied:
                    return render(request, "accounts/account_actions/update_account.html", locals())
            if input_user_id != request.session['user_id']:
                message, is_occupied = Users.is_user_duplicate(
                    user_id=input_user_id)
                if is_occupied:
                    return render(request, "accounts/account_actions/update_account.html", locals())

            Users.update_user_by_user_id(old_user_id=request.session['user_id'], user_id=input_user_id, password=input_password, first_name=input_first_name,
                                         last_name=input_last_name, gender=input_gender, email=input_email, phone=input_phone, city=input_city, birth_date=input_birth_date)

            user = Users.get_user_by_user_id(input_user_id)[0]
            # user = Users.get_user_by_user_id(input_user_id).first()
            request.session['user_id'] = user.user_id
            message = 'Successfully Update Your Account'

    user_id = request.session['user_id']
    init_value = {
        'user_id': user.user_id,  # Must include, but not show for edit
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'email': user.email,
        'phone': user.phone,
        'city': user.city,
        'birth_date': user.birth_date
    }
    update_form = SignUpForm(initial=init_value)
    return render(request, "accounts/account_actions/update_account.html", locals())

def delete_account_view(request):
    if request.method == "POST":
        if request.POST['submit'] == "Delete My Account":
            user_id = request.session['user_id']
            with connections['default'].cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_id='%s';" % user_id)

            request.session.flush()
            return render(request, 'index.html', locals())

        elif request.POST['submit'] == "Let me reconsider it...":
            return render(request, 'index.html', locals())

    return render(request, "accounts/account_actions/delete_account.html", locals())

def personal_image_view(request):
    if request.method  == "POST":
        personalimage = PersonalpicForm(request.POST, request.FILES)

        if personalimage.is_valid():
            return render(request, 'accounts/account_actions/account_image.html',locals(),{'form':personalimage})
    # else:
    user_id = request.session['user_id']
    user = Users.get_user_by_user_id(user_id=user_id)[0]
    personalimage = PersonalpicForm(request.POST, request.FILES)
    context = {
        "user": user,
        "form": personalimage
    }
    return render(request, 'accounts/account_actions/account_image.html',locals(),context)
