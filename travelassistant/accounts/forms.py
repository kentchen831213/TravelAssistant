# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm


# class UserCreateForm(UserCreationForm):

#     class Meta:
#         fields = ('username','email','password1','password2')
#         model = get_user_model()


#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.fields['username'].label = 'Display Name'
#         self.fields['email'].label = "Email Address"

from django import forms
from .models import Users
# from captcha.fields import CaptchaField


class LogInForm(forms.Form):
    user_id = forms.CharField(label="UserID", max_length=128)
    password = forms.CharField(
        label="Password", max_length=256, widget=forms.PasswordInput)
    # captcha = CaptchaField(label='Verification code')


class SignUpForm(forms.Form):
    # class Meta:
    #     model = Users
        gender = [
            ('male', 'male'),
            ('female', 'female'),
        ]
        user_id = forms.CharField(label="UserID", max_length=128,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
        first_name = forms.CharField(label="First Name", max_length=128, widget=forms.TextInput(
            attrs={'class': 'form-control'}))
        last_name = forms.CharField(label="Last Name", max_length=128, widget=forms.TextInput(
            attrs={'class': 'form-control'}))
        gender = forms.ChoiceField(label='Gender', choices=gender)
        email = forms.EmailField(
            label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
        phone = forms.CharField(label="Phone", max_length=128, widget=forms.TextInput(
            attrs={'class': 'form-control'}))
        city = forms.CharField(label="City", max_length=128, widget=forms.TextInput(
            attrs={'class': 'form-control'}))
        birth_date = forms.DateField(label="Birth Date", widget=forms.DateInput(
            attrs={'class': 'form-control'}))

        password = forms.CharField(label="Password", max_length=255,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        password_validation = forms.CharField(label="Confirm Password", max_length=255,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        personal_pic = forms.ImageField(label="Personal Pic", widget=forms.FileInput(
            attrs={'class': 'form-control-file'}))
    # captcha = CaptchaField(label='Verification code')
