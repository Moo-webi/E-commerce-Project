from django.shortcuts import render
import stripe   

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Calculate total paid amount
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),  # Stripe expects amount in cents
                currency='USD',  # Adjust currency as needed
                description='Charge from Djackets',
                source=serializer.validated_data['stripe_token']  # Stripe token from client
            )

            # Save order after successful charge
            serializer.save(user=request.user, paid_amount=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Catch Stripe-specific exceptions
        except stripe.error.CardError as e:
            return Response({'error': 'Card was declined.'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'error': 'An error occurred with the payment.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
