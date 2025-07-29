import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

payload = {
    "username": "test123",
    "first_name": "abc",
    "last_name": "edf",
    "email": "test123@gmail.com",
    "phone_number": "01011112222",
    "password": "test123!",
}

SIGN_UP_URL = "/api/v1/users/sign-up"

# SignUpView Tests - required fields: username, password, first_name, last_name, email, phone_number


# Success
# - creates user with valid input
@pytest.mark.django_db
def test_signup_success():
    client = APIClient()
    response = client.post(SIGN_UP_URL, payload)

    expected_user = {k: v for k, v in payload.items() if k != "password"}

    assert response.status_code == 201
    assert response.data["user"] == expected_user


# Failure
# 1. missing required field(s)
@pytest.mark.parametrize("missing_field", ["username", "first_name", "last_name", "email", "phone_number", "password"])
@pytest.mark.django_db
def test_missing_fields(missing_field):
    client = APIClient()

    # Remove one field at a time
    test_data = {k: v for k, v in payload.items() if k != missing_field}
    response = client.post(SIGN_UP_URL, test_data)

    assert response.status_code == 400
    assert missing_field in response.data


# 2. username already exists
@pytest.mark.django_db
def test_duplicate_username():
    User.objects.create_user(**payload)

    client = APIClient()
    response = client.post(
        SIGN_UP_URL,
        payload={
            "username": "test123",  # duplicate username
            "first_name": "abcde",
            "last_name": "edfef",
            "email": "test12345@gmail.com",
            "phone_number": "01011112244",
            "password": "test123@",
        },
    )

    assert response.status_code == 400
    assert "username" in response.data


# 3. email already exists
@pytest.mark.django_db
def test_duplicate_email():
    User.objects.create_user(**payload)

    client = APIClient()
    response = client.post(
        SIGN_UP_URL,
        payload={
            "username": "test456",
            "first_name": "abcd",
            "last_name": "edfg",
            "email": "test123@gmail.com",  # duplicate email
            "phone_number": "01011112222",
            "password": "test123!",
        },
    )

    assert response.status_code == 400
    assert "email" in response.data


# 4. invalid password format (e.g., too short or weak)
@pytest.mark.django_db
def test_invalid_password():
    test_data = payload.copy()
    test_data["password"] = "123"

    client = APIClient()
    response = client.post(SIGN_UP_URL, test_data)

    assert response.status_code == 400
    assert "password" in response.data


# 5. invalid phone number format
@pytest.mark.django_db
def test_invalid_phone_number():
    test_data = payload.copy()
    test_data["phone_number"] = "0000000"

    client = APIClient()
    response = client.post(SIGN_UP_URL, test_data)

    assert response.status_code == 400
    assert "phone_number" in response.data


# 6. invalid email format
@pytest.mark.django_db
def test_invalid_email():
    test_data = payload.copy()
    test_data["email"] = "00000.com"

    client = APIClient()
    response = client.post(SIGN_UP_URL, test_data)

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
