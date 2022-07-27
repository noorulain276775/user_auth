from django import forms
from accounts.models import *


class UserSignup(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "phone")

    first_name = forms.CharField(
        label="First Name", max_length=20, required=True)
    last_name = forms.CharField(
        label="Last Name", max_length=20, required=True)
    phone = forms.CharField(label="Phone", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'e.g. 923xxxxxxxxx'}))
    password = forms.CharField(label="Password", strip=False, required=True,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'e.g. alpha-numeric combination'}),
                               max_length=30)
    confirm_password = forms.CharField(label="Confirm Password", max_length=30,
                                       widget=forms.PasswordInput(), required=True)

class UserLoginForm(forms.Form):
    phone = forms.CharField(label="Phone", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'e.g. 923xxxxxxxxx'}))

    password = forms.CharField(label="Password", strip=False, required=True,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'e.g. alpha-numeric combination'}),
                               max_length=30)

class OTP_Form(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ("otp", )
    otp = forms.CharField(label="Enter your OTP", required=True,
                          widget=forms.PasswordInput(attrs={'placeholder': 'e.g. 123456'}))


class Reset_Password_phones_Form(forms.Form):
    phone = forms.CharField(label="Phone", required=True, widget=forms.TextInput(
        attrs={'placeholder': 'e.g. 923xxxxxxxxx'}))


class ResetPassword(forms.Form):
    new_password = forms.CharField(label="New Password", strip=False, required=True,
                                   widget=forms.PasswordInput(
                                       attrs={'placeholder': 'e.g. alpha-numeric combination'}),
                                   max_length=30)
    confirm_password = forms.CharField(label="Confirm Password", max_length=30,
                                       widget=forms.PasswordInput(), required=True)
