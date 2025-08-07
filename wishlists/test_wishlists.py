import pytest
from rest_framework.test import APIClient

from .models import Wishlist
from users.models import User
from accommodations.models import Accommodation, City

# ----- Constraints ----
WISHLIST_DETAIL_URL = lambda pk: f"/api/v1/wishlists/{pk}"

# ----- Fixtures -----


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_payload():
    return {
        "username": "test123",
        "first_name": "abc",
        "last_name": "edf",
        "email": "test123@gmail.com",
        "phone_number": "01011112222",
        "password": "test123!",
    }


@pytest.fixture
def sample_db(db, user_payload):
    user = User.objects.create(**user_payload)
    city = City.objects.create(name="Seoul")
    accommodation = Accommodation.objects.create(
        name="Hotel A", region="seoul", location="123", city=city, type="hotel"
    )
    wishlist = Wishlist.objects.create(user=user, name="wishlist")
    wishlist.accommodations.set([accommodation])
    return {"user": user, "accommodation": accommodation, "wishlist": wishlist}


@pytest.fixture
def authenticated_client(client, sample_db):
    user = sample_db["user"]
    client.force_login(user)
    return client


# ----- WishlistDetailView Test -----
# Success
@pytest.mark.django_db
def test_get_wishlist_detail_success(authenticated_client, sample_db):
    wishlist = sample_db["wishlist"]
    response = authenticated_client.get(WISHLIST_DETAIL_URL(wishlist.pk))

    assert response.status_code == 200
    assert response.data["name"] == wishlist.name


# Failure 1
@pytest.mark.django_db
def test_get_wishlist_detail_not_found(authenticated_client):
    response = authenticated_client.get(WISHLIST_DETAIL_URL("200"))
    assert response.status_code == 404


# Failure 2
@pytest.mark.django_db
def test_get_wishlist_detail_no_permission(client, sample_db, user_payload):
    wishlist = sample_db["wishlist"]
    user_payload.update({"username": "test2", "email": "test2@gmail.com"})
    new_user = User.objects.create(**user_payload)
    client.force_login(new_user)
    response = client.get(WISHLIST_DETAIL_URL(wishlist.pk))

    assert response.status_code == 403
    assert response.data["error"] == "You do not have a permission to access this wishlist"


# Success
@pytest.mark.django_db
def test_delete_wishlist_detail_success(authenticated_client, sample_db):
    wishlist = sample_db["wishlist"]
    response = authenticated_client.delete(WISHLIST_DETAIL_URL(wishlist.pk))
    assert response.status_code == 204


# Failure:
@pytest.mark.django_db
def test_delete_wishlist_detail_no_permission(client, sample_db, user_payload):
    wishlist = sample_db["wishlist"]
    user_payload.update({"username": "test2", "email": "test2@gmail.com"})
    new_user = User.objects.create(**user_payload)
    client.force_login(new_user)
    response = client.delete(WISHLIST_DETAIL_URL(wishlist.pk))

    assert response.status_code == 403
    assert response.data["error"] == "You do not have a permission to access this wishlist"


# Success
@pytest.mark.django_db
def test_edit_wishlist_detail_success(authenticated_client, sample_db):
    new_name = {"name": "new wishlist"}
    wishlist = sample_db["wishlist"]
    response = authenticated_client.put(WISHLIST_DETAIL_URL(wishlist.pk), new_name)

    assert response.status_code == 200
    assert response.data["name"] == new_name["name"]


# Failure
@pytest.mark.django_db
def test_edit_wishlist_detail_missing_name_field(authenticated_client, sample_db):
    wishlist = sample_db["wishlist"]
    response = authenticated_client.put(WISHLIST_DETAIL_URL(wishlist.pk))

    assert response.status_code == 400
    assert response.data["name"][0] == "This field is required"
