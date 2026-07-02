from django.db import models
from django.contrib.auth.models import User
from core.models import PrefixedIDModel


class Subscription(PrefixedIDModel):
    id_prefix = "rsub-"
    FREE = "free"
    PAID = "paid"
    PLAN_CHOICES = [(FREE, "Free"), (PAID, "Paid")]

    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    STATUS_CHOICES = [(ACTIVE, "Active"), (CANCELLED, "Cancelled"), (EXPIRED, "Expired")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default=FREE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    started_at = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.plan}"

class PointsTransaction(PrefixedIDModel):
    id_prefix = "rptx-"
    SIGNUP_BONUS = "signup_bonus"
    PURCHASE = "purchase"
    BOOST_SPEND = "boost_spend"
    REASON_CHOICES = [
        (SIGNUP_BONUS, "Signup bonus"),
        (PURCHASE, "Purchase"),
        (BOOST_SPEND, "Boost spend"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="points_transactions")
    amount = models.IntegerField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.amount:+d} ({self.reason})"


class PointsPurchase(PrefixedIDModel):
    id_prefix = "rpur-"
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    STATUS_CHOICES = [(PENDING, "Pending"), (PAID, "Paid"), (FAILED, "Failed")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="points_purchases")
    points = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    reference = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} buys {self.points} pts ({self.status})"