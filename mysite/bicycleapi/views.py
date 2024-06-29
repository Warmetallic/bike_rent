from rest_framework.viewsets import ModelViewSet
from bicycleapi.models import Bicycle, Rental
from bicycleapi.serializers import (
    BicycleSerializer,
    BicycleRentalSerializer,
    BicycleReturnSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.views import extend_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .tasks import calculate_rental_cost


class BicycleListView(ModelViewSet):

    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["id", "name", "model", "status"]
    search_fields = ["name", "model", "status"]
    ordering_fields = ["id", "name", "model", "status"]

    @extend_schema(
        summary="List all bicycles",
        description="Retrieves a list of all bicycles in the system.",
        responses={200: BicycleSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new bicycle",
        description="Create a new **bicycle**",
        request=BicycleSerializer,
        responses=BicycleSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a bicycle by ID",
        description="Get a **bicycle** by ID",
        responses={
            200: BicycleSerializer,
            404: OpenApiResponse(description="Bicycle not found"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a bicycle",
        description="Update an existing **bicycle**",
        request=BicycleSerializer,
        responses=BicycleSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update a bicycle",
        description="Partial update an existing **bicycle**",
        request=BicycleSerializer,
        responses=BicycleSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a bicycle",
        description="Delete an existing **bicycle**",
        responses={204: OpenApiResponse(description="No Content")},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BicycleRental(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Rent a bicycle",
        description="Rent a bicycle by providing the bicycle ID",
        request=BicycleRentalSerializer,
        responses={
            200: OpenApiResponse(description="Bicycle rented successfully"),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Bicycle not found"),
            409: OpenApiResponse(description="User already has an active rental"),
        },
    )
    def post(self, request, *args, **kwargs):
        bicycle_id = request.data.get("bicycle_id")
        # Validate bicycle_id
        if not bicycle_id or bicycle_id <= 0:
            return Response(
                {"error": "Invalid bicycle ID."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user already has an active rental
        if Rental.objects.filter(user=request.user, end_time__isnull=True).exists():
            return Response(
                {"error": "User already has an active rental."},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            bicycle = Bicycle.objects.get(id=bicycle_id, status="available")
        except Bicycle.DoesNotExist:
            return Response(
                {"error": "Bicycle not available or does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Update bicycle status to 'rented'
        bicycle.status = "rented"
        bicycle.save()

        # Create a Rental record
        rental = Rental.objects.create(
            user=request.user,
            bicycle=bicycle,
            start_time=timezone.now(),
            price=10.00,  # Assuming a fixed price for simplicity; adjust as needed
        )

        return Response(
            {"message": "Bicycle rented successfully", "rental_id": rental.id},
            status=status.HTTP_200_OK,
        )


class BicycleReturn(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Return a bicycle",
        description="Return a rented bicycle by providing the rental ID",
        request=BicycleReturnSerializer,
        responses={
            200: OpenApiResponse(description="Bicycle returned successfully"),
            400: OpenApiResponse(description="Bad request"),
            404: OpenApiResponse(description="Rental not found"),
            409: OpenApiResponse(description="Bicycle already returned"),
        },
    )
    def post(self, request, *args, **kwargs):
        rental_id = request.data.get("rental_id")
        if not rental_id:
            return Response(
                {"error": "Rental ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rental = Rental.objects.get(
                id=rental_id, user=request.user, end_time__isnull=True
            )
        except Rental.DoesNotExist:
            return Response(
                {"error": "Rental not found or already returned."},
                status=status.HTTP_404_NOT_FOUND,
            )

            # Calculate rental duration
        rental_end_time = timezone.now()
        rental_duration = rental_end_time - rental.start_time
        rental_duration_hours = rental_duration.total_seconds() / 3600

        # Calculate rental cost (assuming a rate of $5 per hour)
        hourly_rate = 5
        rental_cost = hourly_rate * rental_duration_hours

        # Update rental record with end time and cost
        rental.end_time = rental_end_time
        rental.cost = rental_cost
        rental.bicycle.status = "available"
        rental.bicycle.save()
        rental.save()

        total_hours = int(rental_duration_hours)
        total_minutes = int((rental_duration_hours - total_hours) * 60)

        calculate_rental_cost.delay(rental.bicycle.id, total_hours)

        return Response(
            {
                "message": "Bicycle returned successfully",
                "Total time": f"{total_hours} hours {total_minutes} minutes",
                "Cost": f"${rental_cost:.2f}",
            },
            status=status.HTTP_200_OK,
        )
