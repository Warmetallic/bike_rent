import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_new_user_in_db():
    """
    Test to ensure that a new user can be successfully created and saved in the database.
    """
    User = get_user_model()
    client = APIClient()
    url = reverse("myauthapi:users-list")
    new_user_data = {
        "username": "newuser123",
        "email": "newuser123@example.com",
        "password": "newpassword123",
    }
    response = client.post(url, new_user_data)

    # Verify response status code is HTTP 201 Created
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the user is created in the database
    assert User.objects.filter(email="newuser123@example.com").exists()


@pytest.mark.django_db
def test_login():
    # Access the custom user model
    User = get_user_model()
    # Create a user with the provided username, email, and password
    User.objects.create_user(
        username="wRHelTJS63zh158gi28gK5Eb9Y34WwBeq3cH8yZB.EdYAcfY-yliCvGK5MgZUKrMeRasaoj1SLa5+E2Pkmv9gTBPTfKRpAi6yh+_",
        email="user@example.com",
        password="string",
    )

    client = APIClient()
    url = reverse("myauthapi:login")
    login_data = {"email": "user@example.com", "password": "string"}
    response = client.post(url, login_data)
    assert response.status_code == status.HTTP_200_OK
    # Add more assertions here based on your actual response structure


@pytest.mark.django_db
def test_duplicate_email():
    User = get_user_model()
    User.objects.create_user(
        username="existinguser", email="existing@example.com", password="test"
    )
    client = APIClient()
    url = reverse("myauthapi:users-list")
    duplicate_user_data = {
        "username": "testuser2",
        "email": "existing@example.com",
        "password": "test",
    }
    response = client.post(url, duplicate_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_user_deletion():
    User = get_user_model()
    user = User.objects.create_user(
        username="deletableuser", email="deletable@example.com", password="test"
    )
    client = APIClient()
    url = reverse("myauthapi:users-detail", args=[user.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Optionally, verify user is deleted
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
