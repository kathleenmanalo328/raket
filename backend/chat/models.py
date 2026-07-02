from django.db import models
from django.contrib.auth.models import User
from core.models import PrefixedIDModel

class Conversation(PrefixedIDModel):
    id_prefix="rc-"
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation #{self.pk}"


class Message(PrefixedIDModel):
    id_prefix = "rmsg-"
    TEXT = "text"
    JOB_QUOTE = "job_quote"
    CONTRACT = "contract"
    DELIVERABLE = "deliverable"
    SYSTEM = "system"
    TYPE_CHOICES = [
        (TEXT, "text"),
        (JOB_QUOTE, "job_quote"),
        (CONTRACT, "contract"),
        (DELIVERABLE, "deliverable"),
        (SYSTEM, "system"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TEXT)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to="chat_files/", null=True, blank=True)
    job_post = models.ForeignKey("jobs.JobPost", on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_messages")
    contract =  models.ForeignKey("contracts.Contract", on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    deliverable = models.ForeignKey("contracts.Deliverable", on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message_type}"