from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (

    UserSerializer,
    SMSVerificationSerializer,
)
from django.utils.translation import gettext as _

from ..tasks import task_send_otp
from utils.otp import get_client_ip, otp_generator

class Register(APIView):
    """
    post:
        Send mobile number for Register.
        parameters: [phone,username,password,first_name,last_name]
    """

    permission_classes = [AllowAny]
    throttle_scope = "authentication"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        received_phone = user.phone_number
        ip = get_client_ip(request)
        code = otp_generator()

        # The otp code is sent to the user's phone number for authentication
        res = task_send_otp.delay(ip, code, received_phone)
        if res:
            cache.set(f"{ip}-for-authentication", received_phone, 120)
            cache.set(received_phone, code, 120)
            print(code)
            return Response(_("Code was sent successfully"), status=status.HTTP_200_OK)
        else:
            return Response(_("Code wasn't sent successfully"), status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    """
    post:
        Send otp code to verify mobile number and complete registration.
        parameters: [otp,]
    """

    permission_classes = [AllowAny]
    throttle_scope = "verify_authentication"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request):
        serializer = SMSVerificationSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.data.get("code")
            ip = get_client_ip(request)
            phone = cache.get(f"{ip}-for-authentication")
            otp = cache.get(phone)

            if otp is not None:
                if otp == received_code:
                    user, created = get_user_model().objects.get_or_create(phone_number=phone)
                    user.is_active = True
                    user.save()
                    cache.delete(phone)
                    cache.delete(f"{ip}-for-authentication")

                    context = {
                        _("status"): _("Account successfully created."),
                    }
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            _("incorrect code"): _("The code entered is incorrect."),
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {
                        _("expired code"): _("The code has expired."),
                    },
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )