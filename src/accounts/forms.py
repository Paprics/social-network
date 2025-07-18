from django import forms
from django.contrib.auth import get_user_model


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["phone_number", "email"]


class LoginForm(forms.Form):
    class Meta:
        model = get_user_model()
        fields = ["phone_number"]
