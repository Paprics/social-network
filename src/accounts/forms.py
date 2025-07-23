from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            "phone_number",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email


class LoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["phone_number"]
