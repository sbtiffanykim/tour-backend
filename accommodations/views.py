from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch
from datetime import datetime, date, timedelta
from .models import Accommodation
from room_types.models import RoomType
from packages.models import Package, PackagePrice
from .serializers import AccommodationListSerializer, AccommodationDetailSerializer, AllPackageCombinationsSerializer
from users.models import User


class AccommodationListView(ListAPIView):
    """API view to retrieve a list of accommodations"""

    serializer_class = AccommodationListSerializer

    def get_queryset(self):
        region = self.request.query_params.get("region")
        queryset = Accommodation.objects.all()
        if region:
            queryset = queryset.filter(region=region)
        return queryset

    def list(self, request, *args, **kwargs):
        accommodations = self.get_queryset()
        region = self.request.query_params.get("region", "all")
        if not accommodations.exists():
            return Response({"error": "No accommodations found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(accommodations, many=True)
        return Response({"region": region, "data": serializer.data}, status=status.HTTP_200_OK)


class AccommodationDetailView(APIView):
    """API view to retrieve an accommodation detailed info"""

    def get(self, request, pk):
        try:
            accommodation = Accommodation.objects.get(pk=pk)
        except Accommodation.DoesNotExist:
            raise NotFound("Accommodation not found")
        serializer = AccommodationDetailSerializer(accommodation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllPackageCombinationsView(APIView):
    """Returns all room_type + package combinations for a given accommodation regardless of availability or selected date"""

    def get(self, request, pk):

        if not Accommodation.objects.filter(pk=pk).exists():
            raise NotFound("Accommodation not found")
        combinations = RoomType.objects.filter(accommodation_id=pk).prefetch_related(
            Prefetch("packages", queryset=Package.objects.filter(is_active=True))
        )
        serializer = AllPackageCombinationsSerializer(combinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""
class AvailablePackageCombinationsViewPreview(APIView):

   
    def get(self, request, pk):
        # Parse query parameters
        check_in_str = request.query_params.get("check_in")
        check_out_str = request.query_params.get("check_out")
        guests = int(request.query_params.get("guests", 2))  # default to 2 guests

        if not check_in_str or not check_out_str:
            return Response({"error": "check_in and check_out are required."}, status=400)

        try:
            check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if check_in >= check_out:
            return Response({"error": "check_out must be after check_in."}, status=400)

        # Cache check
        cache_key = f"available_combinations:{pk}:{check_in}:{check_out}:{guests}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        try:
            accommodation = Accommodation.objects.prefetch_related(
                Prefetch(
                    "room_types",
                    queryset=RoomType.objects.prefetch_related(
                        Prefetch(
                            "packages",
                            queryset=Package.objects.prefetch_related(
                                Prefetch(
                                    "daily_prices",
                                    queryset=PackagePrice.objects.filter(
                                        date__gte=check_in, date__lt=check_out, status="open"  # Only available dates
                                    ),
                                )
                            ),
                        )
                    ),
                )
            ).get(pk=pk)
        except Accommodation.DoesNotExist:
            raise NotFound("Accommodation not found.")

        num_nights = (check_out - check_in).days
        date_range = [check_in + timedelta(days=i) for i in range(num_nights)]

        results = []

        for room_type in accommodation.room_types.all():
            if guests > room_type.max_occupancy:
                continue

            for package in room_type.packages.all():
                prices = {p.date: p.price for p in package.daily_prices.all()}
                if all(d in prices for d in date_range):
                    total_price = sum(prices[d] for d in date_range)
                    results.append(
                        {
                            "room_type": room_type.name,
                            "package": package.name,
                            "total_price": total_price,
                            "nights": num_nights,
                            "dates": [d.strftime("%Y-%m-%d") for d in date_range],
                        }
                    )

        # Cache and return response
        cache.set(cache_key, results, timeout=60 * 5)
        return Response(results)
  """


class AvailablePackageCombinationsView(APIView):
    """
    Returns a list of room_type + package combinations that are available
    for a given accommodation based on check-in/check-out dates and guest count.
    Excludes packages that are marked as 'closed' on any of the selected dates.
    """

    def get(self, request, pk):
        # Parse query parameters
        check_in_str = request.query_params.get("check_in")
        check_out_str = request.query_params.get("check_out")
        guests = int(request.query_params.get("guests", 2))

        # If both dates are missing, set default to today and tomorrow
        if not check_in_str and not check_out_str:
            check_in_str = f"{timezone.now().date()}"
            check_out_str = f"{(timezone.now() + timedelta(days=1)).date()}"

        # If only one of the dates is provided, raise an error
        elif (check_in_str and not check_out_str) or (not check_in_str and check_out_str):
            raise ValidationError("Both 'check_in' and 'check_out' must be provided together")

        try:
            # Parse the date strings into date objects
            check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD")

        # Validate that check_in is before check_out
        if check_in >= check_out:
            raise ValidationError("'check_in' must be earlier than 'check_out'")

        # Cache check : later

        # room_type_package 컴비네이션 가지고 오자
        # 날짜 고려: check_in, out
        # 게스트 고려
        try:
            combinations = RoomType.objects.filter(
                accommodation_id=pk, base_occupancy__lte=guests, max_occupancy__gte=guests
            ).prefetch_related(
                Prefetch(
                    "packages",
                    queryset=Package.objects.prefetch_related(
                        Prefetch("daily_prices", queryset=PackagePrice.objects.filter())
                    ),
                )
            )
        except:
            pass

        return Response({"ok": "ok"}, status=status.HTTP_200_OK)
