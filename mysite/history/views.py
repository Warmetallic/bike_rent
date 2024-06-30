from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bicycleapi.models import Rental
from .serializers import RentalHistorySerializer
from drf_spectacular.utils import extend_schema
from .tasks import save_user_history
from asgiref.sync import async_to_sync


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

        # Schedule save_user_history to run asynchronously
        async_to_sync(save_user_history)(serializer.data, request.user.email)

        return Response(serializer.data)
