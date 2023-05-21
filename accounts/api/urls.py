from django.urls import path
from .views import Register,VerifyOtp

app_name = "api"

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("verify/", VerifyOtp.as_view(), name="verify-otp"),
]