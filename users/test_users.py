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
LOGIN_URL = "/api/v1/users/login"
LOGOUT_URL = "/api/v1/users/logout"
PROFILE_URL = "/api/v1/users/me"


@pytest.fixture
def authenticated_client(client, base_payload):
    User.objects.create_user(**base_payload)
    login_data = {"username": base_payload["username"], "password": base_payload["password"]}
    client.post(LOGIN_URL, login_data)

    # token might be needed

    return client


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


# Helper
def login(client, payload_override=None):
    login_data = {
        "username": "test123",
        "password": "test123!",
    }
    if payload_override:
        login_data.update(payload_override)
    return client.post(LOGIN_URL, login_data)


# Success
@pytest.mark.django_db
def test_login_success(client, base_payload):
    User.objects.create_user(**base_payload)
    response = login(client)
    assert response.status_code == 200


# Failure 1. missing required field(s)
@pytest.mark.parametrize("missing_fields", ["username", "password"])
@pytest.mark.django_db
def test_login_missing_fields(client, base_payload, missing_fields):
    User.objects.create_user(**base_payload)
    login_data = {
        "username": base_payload["username"],
        "password": base_payload["password"],
    }
    login_data.pop(missing_fields)
    response = client.post(LOGIN_URL, login_data)
    assert response.status_code == 400


# Failure 2. non-existent user
@pytest.mark.django_db
def test_login_nonexistent_user(client):
    response = login(client)
    assert response.status_code == 403


# Failure 3. incorrect password
@pytest.mark.django_db
def test_login_wrong_password(client, base_payload):
    User.objects.create_user(**base_payload)
    response = login(client, {"password": "wrong_password"})
    assert response.status_code == 403


# LogoutView Tests


# Success
@pytest.mark.django_db
def test_logout_success(authenticated_client):
    response = authenticated_client.post(LOGOUT_URL)
    assert response.status_code == 200


# Failure - unauthenticated user attempts logout
def test_logout_fail(client):
    response = client.post(LOGOUT_URL)
    assert response.status_code == 403


# PrivateUserView Tests - fields: username, points, email, first_name, last_name, phone_number, avatar
# Helper
def edit_profile(authenticated_client, payload_override=None):
    default_data = {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
        "avatar": "",
    }
    if payload_override:
        default_data.update(payload_override)
    return authenticated_client.put(PROFILE_URL, default_data)


# Success 1. retrieves user profile (GET)
@pytest.mark.django_db
def test_profile_retrieve_success(authenticated_client):
    response = authenticated_client.get(PROFILE_URL)
    assert response.status_code == 200


# Success 2. updates user profile with valid data (PUT)
@pytest.mark.django_db
def test_profile_update_success(authenticated_client):
    new_email = "abcd@gmail.com"
    response = edit_profile(authenticated_client, {"email": new_email})
    assert response.status_code == 200
    assert response.data["email"] == new_email


# Failure 1. unauthenticated access
@pytest.mark.django_db
def test_profile_retrieve_unauthenticated(client):
    response = client.get(PROFILE_URL)
    assert response.status_code == 403


# Failure 2. invalid update data: duplicate email
@pytest.mark.django_db
def test_profile_update_duplicate_email(authenticated_client):
    User.objects.create_user(
        **{
            "username": "test12",
            "first_name": "abc",
            "last_name": "edf",
            "email": "test12@gmail.com",
            "phone_number": "01011112222",
            "password": "test12!",
        }
    )
    response = edit_profile(authenticated_client, {"email": "test12@gmail.com"})
    assert response.status_code == 400
    assert "email" in response.data


# Failure 3. invalid update data: invalid phone number format
@pytest.mark.django_db
def test_profile_update_invalid_phone_number(authenticated_client):
    updated_data = {"phone_number": "0000000"}
    response = edit_profile(authenticated_client, updated_data)
    assert response.status_code == 400
    assert "phone_number" in response.data


# Failure 4. invalid update data: invalid email format
@pytest.mark.django_db
def test_profile_update_invalid_email(authenticated_client):
    updated_data = {"email": "00000.com"}
    response = edit_profile(authenticated_client, updated_data)
    assert response.status_code == 400
    assert "email" in response.data


# Failure 5. invalid update data: invalid avatar format
@pytest.mark.django_db
def test_profile_update_invalid_avatar_format(authenticated_client):
    updated_data = {"avatar": "111"}
    response = edit_profile(authenticated_client, updated_data)
    assert response.status_code == 400
    assert "avatar" in response.data


# ChangePasswordView Tests - required fields: current_password, new_password, confirm_password

# Success

# Failure
# 1. missing required field(s)
# 2. current password is incorrect
# 3. new password and confirm password do not match
# 4. new password fails validation (e.g., too short, common)
