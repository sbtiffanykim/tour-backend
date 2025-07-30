import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

# ----- Constants -----
User = get_user_model()
SIGN_UP_URL = "/api/v1/users/sign-up"
LOGIN_URL = "/api/v1/users/login"
LOGOUT_URL = "/api/v1/users/logout"
PROFILE_URL = "/api/v1/users/me"
CHANGE_PASSWORD_URL = "/api/v1/users/change-password"


# ----- Fixtures -----
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


@pytest.fixture
def authenticated_client(client, base_payload):
    user = User.objects.create_user(**base_payload)
    client.force_login(user)
    return client


# ----- SignUpView Tests -----


# Helper
def post_signup(client, override_data=None):
    data = {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
        "password": "test123!",
    }
    if override_data:
        data.update(override_data)
    return client.post(SIGN_UP_URL, data)


# Success
@pytest.mark.django_db
def test_signup_success(client):
    response = post_signup(client)

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
    response = post_signup(client, override_data={"email": "test12345@gmail.com", "phone_number": "01011112244"})
    assert response.status_code == 400
    assert "username" in response.data


# Failure 3. email already exists
@pytest.mark.django_db
def test_duplicate_email(client, base_payload):
    User.objects.create_user(**base_payload)
    response = post_signup(client, override_data={"username": "test456", "phone_number": "01011112222"})
    assert response.status_code == 400
    assert "email" in response.data


# Failure 4. invalid password format
@pytest.mark.django_db
def test_invalid_password(client):
    response = post_signup(client, override_data={"password": "123"})
    assert response.status_code == 400
    assert "password" in response.data


# Failure 5. invalid phone number format
@pytest.mark.django_db
def test_invalid_phone_number(client):
    response = post_signup(client, override_data={"phone_number": "0000000"})
    assert response.status_code == 400
    assert "phone_number" in response.data


# Failure 6. invalid email format
@pytest.mark.django_db
def test_invalid_email(client):
    response = post_signup(client, override_data={"email": "00000.com"})
    assert response.status_code == 400
    assert "email" in response.data


# ----- LoginView Tests -----


# Helper
def post_login(client, override_data=None):
    data = {
        "username": "test123",
        "password": "test123!",
    }
    if override_data:
        data.update(override_data)
    return client.post(LOGIN_URL, data)


# Success
@pytest.mark.django_db
def test_login_success(client, base_payload):
    User.objects.create_user(**base_payload)
    response = post_login(client)
    assert response.status_code == 200


# Failure 1. missing required field(s)
@pytest.mark.parametrize("missing_fields", ["username", "password"])
@pytest.mark.django_db
def test_login_missing_fields(client, base_payload, missing_fields):
    User.objects.create_user(**base_payload)
    login_data = {"username": base_payload["username"], "password": base_payload["password"]}
    login_data.pop(missing_fields)
    response = client.post(LOGIN_URL, login_data)
    assert response.status_code == 400


# Failure 2. non-existent user
@pytest.mark.django_db
def test_login_nonexistent_user(client):
    response = post_login(client)
    assert response.status_code == 403


# Failure 3. incorrect password
@pytest.mark.django_db
def test_login_wrong_password(client, base_payload):
    User.objects.create_user(**base_payload)
    response = post_login(client, {"password": "wrong_password"})
    assert response.status_code == 403


# ----- LogoutView Tests -----


# Success
@pytest.mark.django_db
def test_logout_success(authenticated_client):
    response = authenticated_client.post(LOGOUT_URL)
    assert response.status_code == 200


# Failure - unauthenticated user attempts logout
def test_logout_fail(client):
    response = client.post(LOGOUT_URL)
    assert response.status_code == 403


# ----- PrivateUserView Tests -----


# Helper
def put_profile(authenticated_client, override_data=None):
    data = {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
        "avatar": "",
    }
    if override_data:
        data.update(override_data)
    return authenticated_client.put(PROFILE_URL, data)


# Success 1. retrieves user profile (GET)
@pytest.mark.django_db
def test_get_profile_success(authenticated_client):
    response = authenticated_client.get(PROFILE_URL)
    assert response.status_code == 200


# Success 2. updates user profile with valid data (PUT)
@pytest.mark.django_db
def test_update_profile_success(authenticated_client):
    new_email = "abcd@gmail.com"
    response = put_profile(authenticated_client, {"email": new_email})
    assert response.status_code == 200
    assert response.data["email"] == new_email


# Failure 1. unauthenticated access
@pytest.mark.django_db
def test_get_profile_unauthenticated(client):
    response = client.get(PROFILE_URL)
    assert response.status_code == 403


# Failure 2. invalid update data: duplicate email
@pytest.mark.django_db
def test_update_profile_duplicate_email(authenticated_client):
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
    response = put_profile(authenticated_client, {"email": "test12@gmail.com"})
    assert response.status_code == 400
    assert "email" in response.data


# Failure 3. invalid update data: invalid phone number format
@pytest.mark.django_db
def test_update_profile_invalid_phone_number(authenticated_client):
    updated_data = {"phone_number": "0000000"}
    response = put_profile(authenticated_client, updated_data)
    assert response.status_code == 400
    assert "phone_number" in response.data


# Failure 4. invalid update data: invalid email format
@pytest.mark.django_db
def test_update_profile_invalid_email(authenticated_client):
    updated_data = {"email": "00000.com"}
    response = put_profile(authenticated_client, updated_data)
    assert response.status_code == 400
    assert "email" in response.data


# Failure 5. invalid update data: invalid avatar format
@pytest.mark.django_db
def test_update_profile_invalid_avatar(authenticated_client):
    updated_data = {"avatar": "not_a_file"}
    response = put_profile(authenticated_client, updated_data)
    assert response.status_code == 400
    assert "avatar" in response.data


# ----- ChangePasswordView Tests -----


# Helper
def post_change_password(authenticated_client, override_data=None):
    data = {
        "current_password": "test123!",
        "new_password": "test456@",
        "confirm_password": "test456@",
    }
    if override_data:
        data.update(override_data)
    return authenticated_client.post(CHANGE_PASSWORD_URL, data)


# Success
@pytest.mark.django_db
def test_change_password_success(authenticated_client):
    response = post_change_password(authenticated_client)
    assert response.status_code == 200


# Failure 1. missing required field(s)
@pytest.mark.parametrize("missing_field", ["current_password", "new_password", "confirm_password"])
@pytest.mark.django_db
def test_change_password_missing_fields(client, missing_field, base_payload):
    user = User.objects.create_user(**base_payload)
    client.force_login(user)
    password_data = {
        "current_password": "test123!",
        "new_password": "test456@",
        "confirm_password": "test456@",
    }
    password_data.pop(missing_field)
    response = client.post(CHANGE_PASSWORD_URL, password_data)
    assert response.status_code == 400
    assert missing_field in response.data


# Failure 2. current password is incorrect
@pytest.mark.django_db
def test_change_password_wrong_current(authenticated_client):
    response = post_change_password(authenticated_client, {"current_password": "wrong_password"})
    assert response.status_code == 400


# Failure 3. new password and confirm password do not match
@pytest.mark.django_db
def test_change_password_password_mismatch(authenticated_client):
    response = post_change_password(authenticated_client, {"confirm_password": "wrong_password"})
    assert response.status_code == 400


# Failure 4. new password fails validation
@pytest.mark.django_db
def test_change_password_invalid_format(authenticated_client):
    response = post_change_password(authenticated_client, {"new_password": "123", "confirm_password": "123"})
    assert response.status_code == 400
