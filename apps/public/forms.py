from django import forms
from django.contrib.auth.hashers import make_password
from apps.public.models import Account, AccountVerification


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=150)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = ("date_joined",)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return make_password(password)


class AccountVerificationForm(forms.ModelForm):

    class Meta:
        model = AccountVerification
        fields = "__all__"
        exclude = ("created_at",)
