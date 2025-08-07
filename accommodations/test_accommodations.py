import pytest
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from django.utils import timezone

from .models import Accommodation, City
from room_types.models import RoomType
from packages.models import Package, PackageDailyAvailability, AvailabilityStatus

# ----- Constants -----
BASE_URL = "/api/v1/accommodations/"
DETAIL_URL = lambda pk: f"{BASE_URL}{pk}"
ALL_PACKAGES_URL = lambda pk: f"{BASE_URL}{pk}/room-packages"


def build_available_packages_url(pk, check_in=None, check_out=None):
    base = f"{BASE_URL}{pk}/available-room-packages"
    params = []
    if check_in:
        params.append(f"check_in={check_in}")
    if check_out:
        params.append(f"check_out={check_out}")
    return f"{base}?{'&'.join(params)}" if params else base


# ----- Fixtures -----
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_accommodations(db):
    today = timezone.now().date()
    city = City.objects.create(name="Seoul")

    accommodation = Accommodation.objects.create(
        name="Hotel A", region="seoul", location="123", city=city, type="hotel"
    )
    room_type = RoomType.objects.create(accommodation=accommodation, name="Deluxe", base_occupancy=2, max_occupancy=3)
    package = Package.objects.create(room_type=room_type, name="Room Only", price=100000, is_active=True)
    PackageDailyAvailability.objects.create(package=package, date=today, price=120000, status=AvailabilityStatus.OPEN)
    inactive_package = Package.objects.create(room_type=room_type, name="Inactive", price=90000, is_active=False)

    return {
        "accommodation": accommodation,
        "room_type": room_type,
        "package": package,
        "inactive_package": inactive_package,
    }


# ----- AccommodationListView Test -----


# Success 1: All
@pytest.mark.django_db
def test_get_accommodation_list_all_success(client, sample_accommodations):
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.data["data"]) == 1


# Success 2: With region params
@pytest.mark.django_db
def test_get_accommodation_list_with_region_success(client, sample_accommodations):
    response = client.get(BASE_URL, {"region": "seoul"})
    assert response.status_code == 200
    assert "seoul" in response.data["region"]


# Failure: No matching region
@pytest.mark.django_db
def test_get_accommodation_list_no_match(client, sample_accommodations):
    response = client.get(BASE_URL, {"region": "null"})
    assert response.status_code == 404
    assert response.data["error"] == "No accommodations found"


# ----- AccommodationDetailView Test -----


# Success
@pytest.mark.django_db
def test_get_accommodation_detail_success(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
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
@pytest.mark.django_db
def test_get_all_packages_success(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
    response = client.get(ALL_PACKAGES_URL(accommodation.id))

    assert response.status_code == 200
    assert isinstance(response.data, list)


# Failure
@pytest.mark.django_db
def test_get_all_packages_not_found(client, sample_accommodations):
    non_existent_id = 999999
    response = client.get(ALL_PACKAGES_URL(non_existent_id))

    assert response.status_code == 404
    assert response.data["detail"] == "Accommodation not found"


# ----- AvailableRoomPackagesView Test -----


# Success
@pytest.mark.django_db
def test_get_available_packages_success(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
    package = sample_accommodations["package"]
    check_in = timezone.now().date()
    check_out = check_in + timedelta(days=1)
    url = build_available_packages_url(accommodation.id, check_in, check_out)
    response = client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert response.data[0]["name"] == package.name


# Failure1: check_in or check_out missing
@pytest.mark.django_db
def test_get_available_packages_missing_dates(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
    url = build_available_packages_url(accommodation.id, check_in=timezone.now().date())
    response = client.get(url)

    assert response.status_code == 400
    assert response.data["error"] == "Both 'check_in' and 'check_out' must be provided together"


# Failure2: invalid date format
@pytest.mark.django_db
def test_get_available_packages_invalid_date_format(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
    url = build_available_packages_url(accommodation.id, check_in="20250801", check_out="20250802")
    response = client.get(url)

    assert response.status_code == 400
    assert response.data["error"] == "Invalid date format. Use 'YYYY-MM-DD'"


# Failure3: check_in >= check_out
@pytest.mark.django_db
def test_get_available_packages_check_in_after_check_out(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
    today = timezone.now().date()
    url = build_available_packages_url(accommodation.id, check_in=today + timedelta(days=2), check_out=today)
    response = client.get(url)

    assert response.status_code == 400
    assert response.data["error"] == "'check_in' must be earlier than 'check_out'"


# Failure3: No availability on that date - returns empty list
@pytest.mark.django_db
def test_get_available_packages_no_availability(client, sample_accommodations):
    accommodation = sample_accommodations["accommodation"]
    future_date = timezone.now().date() + timedelta(days=30)
    url = build_available_packages_url(accommodation.id, future_date, future_date + timedelta(days=1))
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 0
