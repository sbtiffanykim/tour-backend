import pytest
from rest_framework.test import APIClient
from .models import Accommodation, City
from room_types.models import RoomType
from packages.models import Package

# ----- Constants -----
BASE_URL = "/api/v1/accommodations/"
DETAIL_URL = lambda pk: f"{BASE_URL}{pk}"
ALL_PACKAGES_URL = lambda pk: f"{BASE_URL}{pk}/room-packages"


# ----- Fixtures -----
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_accommodations(db):

    city1 = City.objects.create(name="Seoul")
    city2 = City.objects.create(name="Busan")

    acc1 = Accommodation.objects.create(
        name="Seoul Hotel", location="Seoul 111", region="seoul", city=city1, type="hotel"
    )

    acc2 = Accommodation.objects.create(
        name="Busan Resort", location="Busan 222", region="gyeongsang", city=city2, type="resort"
    )

    # Connect to acc1
    room1 = RoomType.objects.create(accommodation=acc1, name="Deluxe Room", base_occupancy=2, max_occupancy=2)
    Package.objects.create(room_type=room1, name="Room Only", price=80000)

    # Connect to acc2
    room2 = RoomType.objects.create(accommodation=acc2, name="Double Room", base_occupancy=2, max_occupancy=3)
    Package.objects.create(room_type=room2, name="Room Only", price=100000)

    return [acc1, acc2]


# ----- AccommodationListView Test -----


# Success 1: All
def test_get_accommodation_list_all_success(client, sample_accommodations):
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.data["data"]) == 2


# Success 2: With region params
@pytest.mark.parametrize("region", ["seoul", "gyeongsang"])
def test_get_accommodation_list_with_region_success(client, sample_accommodations, region):
    response = client.get(BASE_URL, {"region": region})
    assert response.status_code == 200
    assert region in response.data["region"]


# Failure: No matching region
def test_get_accommodation_list_no_match(client, sample_accommodations):
    response = client.get(BASE_URL, {"region": "null"})
    assert response.status_code == 404
    assert response.data["error"] == "No accommodations found"


# ----- AccommodationDetailView Test -----


# Success
@pytest.mark.django_db
def test_get_accommodation_detail_success(client, sample_accommodations):
    accommodation = sample_accommodations[0]
    response = client.get(DETAIL_URL(accommodation.id))

    assert response.status_code == 200
    assert response.data["id"] == accommodation.id
    assert response.data["name"] == accommodation.name


# Failure
@pytest.mark.django_db
def test_get_accommodation_detail_not_found(client, sample_accommodations):
    non_existent_id = 999999
    response = client.get(DETAIL_URL(non_existent_id))

    assert response.status_code == 404
    assert response.data["detail"] == "Accommodation not found"


# ----- RoomPackageListView Test -----


# Success
def test_get_all_packages_success(client, sample_accommodations):
    accommodation = sample_accommodations[0]
    response = client.get(ALL_PACKAGES_URL(accommodation.id))

    assert response.status_code == 200
    assert isinstance(response.data, list)


# Failure
def test_get_all_packages_not_found(client, sample_accommodations):
    non_existent_id = 999999
    response = client.get(ALL_PACKAGES_URL(non_existent_id))

    assert response.status_code == 404
    assert response.data["detail"] == "Accommodation not found"
