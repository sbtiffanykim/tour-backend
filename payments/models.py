from django.db import models


class PaymentMethod(models.TextChoices):
    """Payment methods available to customers"""

    CARD = "card", "Credit/Debit Card"
    BANK_TRANSFER = "bank_transfer", "Bank_transfer"
    MOBILE = "mobile", "Mobile"
    POINTS = "points", "Points"


class PaymentStatus(models.TextChoices):
    """Customer payment processing status (staff-only view)"""

    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    REFUND_REQUESTED = "refund_requested", "Refund Requested"
    REFUNDED = "refunded", "Refunded"
    CANCEL_REQUESTED = "cancel_requested", "Cancel Requested"
    CANCELLED = "cancelled", "Cancelled"


class SettlementStatus(models.TextChoices):
    """Settlement status with the accommodation partner (staff-only view)"""

    NOT_SETTLED = "not_settled", "Not settled"
    PARTIALLY_SETTLED = "partially_settled", "Partially Settled"
    SETTLED = "settled", "Settled"


class Payment(models.Model):
    """Payment records for a booking. Ensures split payments(e.g., card + points)."""

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    booking = models.ForeignKey("bookings.Booking", on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField(help_text="Amount paid by this method")
    method = models.CharField(max_length=30, choices=PaymentMethod.choices)
    status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    def __str__(self):
        return f"{self.booking} - {self.method} {self.amount} KRW"


class PaymentAdminInfo(models.Model):
    """Staff-only settlement info with accommodations"""

    payment = models.OneToOneField("payments.Payment", on_delete=models.CASCADE, related_name="admin_info")
    settlement_status = models.CharField(
        max_length=30, choices=SettlementStatus.choices, default=SettlementStatus.NOT_SETTLED
    )
    staff_note = models.TextField(blank=True, null=True, max_length=100)

    def __str__(self):
        return f"Admin info for Booking #{self.booking.id}"
