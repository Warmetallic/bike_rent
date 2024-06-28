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

from drf_spectacular.utils import extend_schema


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    request=UserAuthenticationSerializer,
    responses=UserAuthenticationSerializer,
    description="User login",
)
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            # Fetch the user by email
            user = User.objects.get(email=email)
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


@extend_schema(
    request=UserAuthenticationSerializer,
    responses=UserAuthenticationSerializer,
    description="User registration",
)
class UserRegistrationAPIView(APIView):
    def post(self, request):
        user_data = request.data
        user_data["password"] = make_password(user_data["password"])
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def hello_world_view(request) -> Response:
    return Response({"message": "Hello, world!"})


# @api_view()
# def home(request):
#     return render(request, "myauthapi/home.html")
