from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobPost
from core.models import PrefixedIDModel

class Contract(PrefixedIDModel):
    id_prefix="rct-"
    CREATED = "created"
    SIGNED = "signed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (CREATED, "created"),
        (SIGNED, "signed"),
        (DELIVERED, "delivered"),
        (CANCELLED, "cancelled"),
        ]
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="contracts")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts_as_client")
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts_as_contractor")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contracts_created")
    terms = models.TextField(blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CREATED)
    signed_at = models.DateTimeField(null=True, blank=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract #{self.pk} for {self.job_post.title}"

class Deliverable(PrefixedIDModel):
    id_prefix = "rdel-"
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="deliverables")
    file = models.FileField(upload_to="deliverables/")
    preview = models.ImageField(upload_to="deliverable_previews/", null=True, blank=True)
    note = models.TextField(max_length=1000, blank=True)
    is_unlocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deliverable #{self.pk} for contract #{self.contract_id}"

class Payment(PrefixedIDModel):
    id_prefix="rpay-"
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (PENDING, "pending"),
        (PAID, "paid"),
        (FAILED, "failed"),
        (CANCELLED, "cancelled"),
    ]

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="payments")
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    reference = models.CharField(max_length=100, blank=True) #payment provider's transaction id
    updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.pk} ({self.status}) for contract #{self.contract_id}"