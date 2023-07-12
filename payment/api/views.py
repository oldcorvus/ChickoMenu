from rest_framework import generics, status, permissions
from rest_framework.response import Response
from payment.models import Order
from .serializers import OrderSerializer
from plan.models import UserPlan
from .permissions import IsUserPlanOwner
from rest_framework.views import APIView
from django.conf import settings
import requests
import json
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserPlanOwner]
    queryset = Order.objects.all() 


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        # Get the user plan with the given id and is_active=True
        user_plan_id = request.data.get('user_plan_id')  
        try:
            user_plan = UserPlan.objects.get(id=user_plan_id, user=request.user)
        
        except UserPlan.DoesNotExist:
            return Response({"error": _("No active plan found for this user.")}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order for the active user plan
        order = Order.objects.create(
            user_plan=user_plan,
            payable_amount=user_plan.plan.price
        )

        if user_plan.plan.name == 'Free':
            order.is_paid = True
            user_plan.is_active = True
            order.save()
            user_plan.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Get all orders for the current user
        return Order.objects.filter(user_plan__user=self.request.user)


class PaymentView(APIView):
    def post(self, request):
        # Get the order ID from the request data
        order_id = request.data.get('order_id')

        # Get the corresponding order from the database
        try:
            order = Order.objects.get(id=order_id, user_plan__user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'})

        # Get the amount from the order
        amount = order.total_amount

        # Set the ZarinPal API endpoint
        url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

        # Set the data to be sent to the API
        data = {
            'MerchantID': settings.ZARINPAL_MERCHANT_ID,
            'Amount': amount,
            'Description': 'خرید از سایت چیکو',
            'Email': request.user.email,
            'CallbackURL': 'http://localhost:8000/payment/verify/',
            'Metadata': {'order_id': str(order.id)},
        }

        # Send a request to the ZarinPal API
        response = requests.post(url, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            response_data = response.json()

            # Check if the payment was successful
            if response_data.get('Status') == 100:
                # Get the payment URL from the response data
                payment_url = f"https://sandbox.zarinpal.com/pg/StartPay/{response_data.get('Authority')}"

                # Save the payment authority to the database
                order.authority = response_data.get('Authority')
                order.save()

                return Response({'payment_url': payment_url})

        # If the payment was not successful, return an error response
        return Response({'error': 'Payment failed'})

class VerifyPaymentView(APIView):
    def post(self, request):
        # Get the payment information from the request data
        authority = request.data.get('Authority')
        status = request.data.get('Status')

        # Set the ZarinPal API endpoint
        url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'

        # Get the order ID from the payment metadata
        metadata = request.data.get('Metadata')
        order_id = metadata.get('order_id')

        # Get the corresponding order from the database
        try:
            order = Order.objects.get(id=order_id, user_plan__user=request.user)
        except Order.DoesNotExist:
            return Response({'error': _('Order not found')})

        # Set the data to be sent to the API
        data = {
            'MerchantID': settings.ZARINPAL_MERCHANT_ID,
            'Authority': authority,
            'Amount': order.total_amount,
        }

        # Send a request to the ZarinPal API
        response = requests.post(url, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            response_data = response.json()

            # Check if the payment was successful
            if response_data.get('Status') == 100:
                # Save the payment information to the database
                order.authority = response_data.get('Authority')
                order.ref_id = response_data.get('RefID')
                order.is_paid = True
                order.user_plan.is_paid = True
                order.user_plan.save() 
                order.save()

                # Return a success response
                return Response({'success': True})

        # If the payment was not successful, return an error response
        return Response({'error': 'Payment verification failed'})