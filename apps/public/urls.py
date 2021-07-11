from django.urls import path

from apps.public.views import Home, SignIn, Registration, Verification, Dashboard, sign_out

app_name = "public"
urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("sign-in", SignIn.as_view(), name="sign-in"),
    path("registration", Registration.as_view(), name="registration"),
    path("verification/<str:username>", Verification.as_view(), name="verification"),
    path("dashboard", Dashboard.as_view(), name="dashboard"),
    path("sign-out", sign_out, name="sign-out"),
]
