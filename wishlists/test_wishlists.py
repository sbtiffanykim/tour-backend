import pytest
from rest_framework.test import APIClient

from .models import Wishlist
from users.models import User
from accommodations.models import Accommodation, City

# ----- Constraints ----
WISHLIST_DETAIL_URL = lambda pk: f"/api/v1/wishlists/{pk}"
CREATE_WISHLIST_URL = f"/api/v1/wishlists/create"
ADD_ACC_TO_WISHLIST_URL = (
    lambda wishlist_pk, accommodation_pk: f"/api/v1/wishlists/{wishlist_pk}/add/{accommodation_pk}"
)
REMOVE_ACC_FROM_WISHLIST_URL = (
    lambda wishlist_pk, accommodation_pk: f"/api/v1/wishlists/{wishlist_pk}/remove/{accommodation_pk}"
)

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


@pytest.fixture()
def new_accommodation():
    city = City.objects.create(name="Busan")
    return Accommodation.objects.create(name="Resort A", region="busan", location="test", city=city, type="resort")


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


# Failure
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


# ----- CreateWishlistView Test -----
# Success
@pytest.mark.django_db
def test_create_wishlist_success(client, user_payload):
    wishlist_name = {"name": "create wishlist"}
    user_payload.update({"username": "test2", "email": "test2@gmail.com"})
    new_user = User.objects.create(**user_payload)
    client.force_login(new_user)
    response = client.post(CREATE_WISHLIST_URL, wishlist_name)

    assert response.status_code == 201
    assert response.data["name"] == wishlist_name["name"]


# Failure
@pytest.mark.django_db
def test_create_wishlist_already_exist(authenticated_client, sample_db):
    response = authenticated_client.post(CREATE_WISHLIST_URL)

    assert response.status_code == 400
    assert response.data["error"] == "You already have a wishlist"


# ----- AddAccommodationToWishlistView Test -----


# Success
@pytest.mark.django_db
def test_add_acc_to_wishlist_success(authenticated_client, sample_db, new_accommodation):
    initial_num = sample_db["wishlist"].accommodations.count()
    new_accommodation = new_accommodation
    wishlist = sample_db["wishlist"]
    response = authenticated_client.post(ADD_ACC_TO_WISHLIST_URL(wishlist.pk, new_accommodation.pk))

    assert response.status_code == 200
    assert response.data["success"] == "Accommodation added"
    wishlist.refresh_from_db()
    assert wishlist.accommodations.count() == initial_num + 1


# Failure 1: Wishlist does not exist
@pytest.mark.django_db
def test_add_acc_to_wishlist_wishlist_not_found(authenticated_client, new_accommodation):
    new_accommodation = new_accommodation
    non_existent_wishlist_pk = 10000  # assume wishlist with this pk does not exist
    response = authenticated_client.post(ADD_ACC_TO_WISHLIST_URL(non_existent_wishlist_pk, new_accommodation.pk))
    assert response.status_code == 404
    assert response.data["error"] == "Wishlist not found"


# Failure 2: No permission
@pytest.mark.django_db
def test_add_acc_to_wishlist_no_permission(client, sample_db, new_accommodation, user_payload):
    wishlist = sample_db["wishlist"]
    user_payload.update({"username": "test2", "email": "test2@gmail.com"})
    new_user = User.objects.create(**user_payload)
    client.force_login(new_user)
    new_accommodation = new_accommodation
    response = client.post(ADD_ACC_TO_WISHLIST_URL(wishlist.pk, new_accommodation.pk))

    assert response.status_code == 403
    assert response.data["error"] == "You do not have a permission to access this wishlist"


# Failure 3: Accommodation does not exist
@pytest.mark.django_db
def test_add_acc_to_wishlist_acc_not_found(authenticated_client, sample_db):
    wishlist = sample_db["wishlist"]
    non_existent_accommodation_pk = 10000  # assume accommodation with this pk does not exist
    response = authenticated_client.post(ADD_ACC_TO_WISHLIST_URL(wishlist.pk, non_existent_accommodation_pk))
    assert response.status_code == 404
    assert response.data["error"] == "Accommodation not found"


# ----- RemoveAccommodationToWishlistView Test -----


# Success
@pytest.mark.django_db
def test_remove_acc_from_wishlist_success(authenticated_client, sample_db):
    initial_num = sample_db["wishlist"].accommodations.count()
    accommodation = sample_db["accommodation"]
    wishlist = sample_db["wishlist"]
    response = authenticated_client.delete(REMOVE_ACC_FROM_WISHLIST_URL(wishlist.pk, accommodation.pk))

    assert response.status_code == 200
    assert response.data["success"] == "Accommodation removed"
    wishlist.refresh_from_db()
    assert wishlist.accommodations.count() == initial_num - 1


# Failure 1: Wishlist does not exist
@pytest.mark.django_db
def test_remove_acc_from_wishlist_wishlist_not_found(authenticated_client, sample_db):
    accommodation = sample_db["accommodation"]
    non_existent_wishlist_pk = 10000  # assume wishlist with this pk does not exist
    response = authenticated_client.delete(REMOVE_ACC_FROM_WISHLIST_URL(non_existent_wishlist_pk, accommodation.pk))
    assert response.status_code == 404
    assert response.data["error"] == "Wishlist not found"


# Failure 2: No permission
@pytest.mark.django_db
def test_remove_acc_from_wishlist_no_permission(client, sample_db, user_payload):
    wishlist = sample_db["wishlist"]
    user_payload.update({"username": "test2", "email": "test2@gmail.com"})
    new_user = User.objects.create(**user_payload)
    client.force_login(new_user)
    accommodation = sample_db["accommodation"]
    response = client.delete(REMOVE_ACC_FROM_WISHLIST_URL(wishlist.pk, accommodation.pk))

    assert response.status_code == 403
    assert response.data["error"] == "You do not have a permission to access this wishlist"


# Failure 3: Accommodation does not exist
@pytest.mark.django_db
def test_remove_acc_from_wishlist_acc_not_found(authenticated_client, sample_db):
    wishlist = sample_db["wishlist"]
    non_existent_accommodation_pk = 10000  # assume accommodation with this pk does not exist
    response = authenticated_client.delete(REMOVE_ACC_FROM_WISHLIST_URL(wishlist.pk, non_existent_accommodation_pk))
    assert response.status_code == 404
    assert response.data["error"] == "Accommodation not found"
