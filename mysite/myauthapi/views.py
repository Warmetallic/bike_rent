from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, UserAuthenticationSerializer
from django.contrib.auth.models import User

from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from drf_spectacular.utils import extend_schema, OpenApiResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


@extend_schema(
    methods=["get"],  # Apply this extension only to the GET method
    summary="Get User List",
    description="Retrieves a list of all users in the system. Requires authentication.",
    responses={200: UserSerializer(many=True)},
)
class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "id",
        "username",
        "email",
    ]

    search_fields = [
        "username",
        "email",
    ]

    ordering_fields = [
        "id",
        "username",
        "email",
    ]

    @extend_schema(
        summary="Get a user by ID",
        description="Get a **user** by ID",
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="User not found"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new user",
        description="Create a new **user**",
        request=UserSerializer,
        responses=UserSerializer,
    )
    def create(self, request, *args, **kwargs):
        # Handle user registration logic here
        user_data = request.data
        # Check if email is unique
        if User.objects.filter(email=user_data.get("email")).exists():
            return Response(
                {"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST
            )
        # Original line causing error:
        # user_data["password"] = make_password(user_data["password"])

        # Fixed code:
        user_data = request.data.copy()  # Make a mutable copy of the request data
        user_data["password"] = make_password(user_data["password"])
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Update a user",
        description="Update an existing **user**",
        request=UserSerializer,
        responses=UserSerializer,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update a user",
        description="Partial update an existing **user**",
        request=UserSerializer,
        responses=UserSerializer,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a user",
        description="Delete an existing **user**",
        responses={204: OpenApiResponse(description="No Content")},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    summary="User Login",
    description="This endpoint allows users to login by providing their email and password.",
    request=UserAuthenticationSerializer,
    responses={
        200: OpenApiResponse(description="Successful Login"),
        401: OpenApiResponse(description="Unauthorized"),
    },
)
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            # Fetch the user by email
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response(
                {"error": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Now authenticate the user by username
        user = authenticate(username=user.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED
        )
