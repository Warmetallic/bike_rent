from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bicycleapi.models import Rental
from .serializers import RentalHistorySerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Get Rental History",
    description="Get a list of all rentals made by the authenticated user",
    responses={200: RentalHistorySerializer(many=True)},
)
class RentalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rentals = Rental.objects.filter(user=request.user).order_by("-start_time")
        serializer = RentalHistorySerializer(rentals, many=True)
        return Response(serializer.data)
