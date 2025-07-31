import pytest
from rest_framework.test import APIClient
from .models import Accommodation

# ----- Constants -----
LIST_URL = "/api/v1/accommodations/"


# ----- Fixtures -----
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_accommodations(db):
    return [
        Accommodation.objects.create(name="Sample Hotel", location="Sample 123 Street", region="seoul"),
        Accommodation.objects.create(name="Sample Resort", location="Sample 123 Street", region="gyeongsang"),
    ]


# ----- AccommodationListView Test -----


# Success 1: All
def test_get_accommodation_list_all_success(client, sample_accommodations):
    response = client.get(LIST_URL)
    assert response.status_code == 200
    assert len(response.data) == 2


# Success 2: With region params
@pytest.mark.parametrize("region", ["seoul", "gyeongsang"])
def test_get_accommodation_list_with_region_success(client, sample_accommodations, region):
    response = client.get(LIST_URL, {"region": region})
    assert response.status_code == 200
    assert all(item["region"] == region for item in response.data)


# Failure: No matching region
def test_get_accommodation_list_no_match(client, sample_accommodations):
    response = client.get(LIST_URL, {"region": "null"})
    assert response.status_code == 404
    assert response.data["error"] == "No accommodations found"
