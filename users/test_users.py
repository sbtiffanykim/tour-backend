import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def base_payload():
    return {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
        "password": "test123!",
    }


User = get_user_model()
SIGN_UP_URL = "/api/v1/users/sign-up"

# SignUpView Tests - required fields: username, password, first_name, last_name, email, phone_number


# Helper
def signup(client, payload_override=None):
    data = {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
        "password": "test123!",
    }
    if payload_override:
        data.update(payload_override)
    return client.post(SIGN_UP_URL, data)


# Success
@pytest.mark.django_db
def test_signup_success(client):
    response = signup(client)

    expected = {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
    }

    assert response.status_code == 201
    assert response.data["user"] == expected


# Failure 1. missing required field(s)
@pytest.mark.parametrize("missing_field", ["username", "first_name", "last_name", "email", "phone_number", "password"])
@pytest.mark.django_db
def test_missing_fields(client, missing_field, base_payload):
    # Remove one field at a time
    base_payload.pop(missing_field)
    response = client.post(SIGN_UP_URL, base_payload)
    assert response.status_code == 400
    assert missing_field in response.data


# Failure 2. username already exists
@pytest.mark.django_db
def test_duplicate_username(client, base_payload):
    User.objects.create_user(**base_payload)
    response = signup(client, payload_override={"email": "test12345@gmail.com", "phone_number": "01011112244"})
    assert response.status_code == 400
    assert "username" in response.data


# Failure 3. email already exists
@pytest.mark.django_db
def test_duplicate_email(client, base_payload):
    User.objects.create_user(**base_payload)
    response = signup(client, payload_override={"username": "test456", "phone_number": "01011112222"})
    assert response.status_code == 400
    assert "email" in response.data


# Failure 4. invalid password format
@pytest.mark.django_db
def test_invalid_password(client):
    response = signup(client, payload_override={"password": "123"})
    assert response.status_code == 400
    assert "password" in response.data


# Failure 5. invalid phone number format
@pytest.mark.django_db
def test_invalid_phone_number(client):
    response = signup(client, payload_override={"phone_number": "0000000"})
    assert response.status_code == 400
    assert "phone_number" in response.data


# Failure 6. invalid email format
@pytest.mark.django_db
def test_invalid_email(client):
    response = signup(client, payload_override={"email": "00000.com"})
    assert response.status_code == 400
    assert "email" in response.data


# LoginView Tests - required fields: username, password

# Success
# - logs in with valid credentials

# Failure
# 1. missing required field(s)
# 2. non-existent user
# 3. incorrect password


# LogoutView Tests

# Success
# - logs out authenticated user

# Failure
# - unauthenticated user attempts logout


# PrivateUserView Tests - fields: username, points, email, first_name, last_name, phone_number, avatar

# Success
# 1. retrieves user profile (GET)
# 2. updates user profile with valid data (PUT)

# Failure
# 1. unauthenticated access
# 2. invalid update data:
#    2-1. duplicate email
#    2-2. invalid phone number format
#    2-3. invalid email format
#    2-4. invalid avatar format (e.g., not an image)


# ChangePasswordView Tests - required fields: current_password, new_password, confirm_password

# Success
# - changes password with valid input

# Failure
# 1. missing required field(s)
# 2. current password is incorrect
# 3. new password and confirm password do not match
# 4. new password fails validation (e.g., too short, common)
