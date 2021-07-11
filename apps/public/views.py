import uuid

from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
import random

from apps.public.forms import SignInForm, RegistrationForm, AccountVerificationForm
from apps.public.models import Account, AccountVerification
from config.utility import form_error


class Home(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect("public:dashboard")
        return render(request, "public/home.html")


class SignIn(View):

    @staticmethod
    def post(request):
        form = SignInForm(data={
            "email": request.POST.get("user-email"),
            "password": request.POST.get("user-password")
        })
        if form.is_valid():
            try:
                user = Account.objects.get(email=form.cleaned_data.get("email"))
            except Account.DoesNotExist:
                messages.error(request, "User does not exists", extra_tags="bg-red-400")
            else:
                if user.is_active:
                    if check_password(form.cleaned_data.get("password"), user.password):
                        login(request, user)
                        messages.success(request, "Successfully logged in", extra_tags="bg-green-400")
                        return redirect("public:dashboard")
                    messages.error(request, "Password did not matched. Try again.", extra_tags="bg-red-400")
                else:
                    messages.info(request, "Please wait for your account to be activated", extra_tags="bg-indigo-400")
        for error in form_error(form.errors.get_json_data()):
            messages.error(request, error, extra_tags="bg-red-400")
        return redirect("public:home")


class Registration(View):

    @staticmethod
    def get(request):
        messages.info(request, "Please complete your registration process here", extra_tags="bg-indigo-500")
        return redirect("public:home")

    def post(self, request):
        form = RegistrationForm(data={
            "first_name": request.POST.get("first-name"),
            "last_name": request.POST.get("last-name"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "username": uuid.uuid4()
        })
        if form.is_valid():
            if check_password(request.POST.get("confirm-password"), form.cleaned_data.get("password")):
                account = form.save()
                verification_code = self.new_verification_code()
                try:
                    account_verification = AccountVerification.objects.get(account=account)
                except AccountVerification.DoesNotExist:
                    AccountVerification.objects.create(
                        account=account,
                        code=verification_code
                    )
                else:
                    account_verification.code = verification_code
                    account_verification.save()
                send_mail(
                    subject="Activate your account!",
                    message=f"Your verification code is: {verification_code}",
                    from_email="md.rifaetullahrifat@gmail.com",
                    recipient_list=[account.email],
                    fail_silently=False
                )
                messages.error(request, "Please check your email to activate your account", extra_tags="bg-green-500")
                return redirect("public:verification", account.username)
            messages.info(request, "Password did not matched", extra_tags="bg-yellow-500")
        else:
            for error in form_error(form.errors.get_json_data()):
                messages.error(request, error, extra_tags="bg-red-500")
        return redirect("public:home")

    @staticmethod
    def new_verification_code():
        return random.randint(111111, 999999)


class Verification(View):

    @staticmethod
    def get(request, username):
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            messages.error(request, "Invalid user. Please sign up.", extra_tags="bg-red-400")
            return redirect("public:home")
        else:
            if account.is_active:
                messages.info(request, "Your account is already activated. Try sing in.", extra_tags="bg-indigo-400")
                # return redirect("public:home")
        context = {"username": username}
        return render(request, "public/verification.html", context)

    @staticmethod
    def post(request, username):
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            messages.error(request, "User does not exist", extra_tags="bg-red-400")
        else:
            form = AccountVerificationForm(data={
                "account": account,
                "code": request.POST.get("verification-code")
            })
            if form.is_valid():
                account_verification = account.accountverification_set.first()
                if not account_verification:
                    messages.info(request, "Something went wrong. Try again.", extra_tags="bg-yellow-400")
                elif account_verification.code == form.cleaned_data.get("code"):
                    account.is_active = True
                    account.save()
                    account_verification.delete()
                    messages.success(request, "Your account is now activated. Sign in.", extra_tags="bg-green-400")
                    return redirect("public:home")
                else:
                    messages.info(request, "Invalid verification code. Try again.", extra_tags="bg-yellow-400")
            else:
                for error in form_error(form.errors.get_json_data()):
                    messages.error(request, error, extra_tags="bg-red-400")
        return redirect("public:verification", username)


class Dashboard(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        return render(request, "public/dashboard.html")


def sign_out(request):
    logout(request)
    messages.success(request, "Successfully signed out")
    return redirect("public:home")
