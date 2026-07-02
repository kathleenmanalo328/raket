import mimetypes
from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobPost
from core.models import PrefixedIDModel

class FeedPost(PrefixedIDModel):
    id_prefix = "rfp-"
    IMAGE="image"
    VIDEO="video"
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feed_posts", null=True, blank=True)
    caption = models.TextField(max_length=1000, blank=False)
    file = models.FileField(upload_to="posts/", blank=True)
    media_type = models.CharField(max_length=10, default=IMAGE, editable=False)
    job_post = models.OneToOneField(JobPost, on_delete=models.SET_NULL, null=True, blank=True, related_name="feed_posts")
    shares_count = models.PositiveIntegerField(default=0)
    reposts_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            guessed, _ = mimetypes.guess_type(self.file.name)
            self.media_type =  self.VIDEO if (guessed or "").startswith("video") else self.IMAGE
        super().save(*args, **kwargs)

    def __str__(self):
        username = self.author.username if self.author else "anon"
        return f"{username}'s post #{self.pk}"

class Comment(PrefixedIDModel):
    id_prefix = "rcom-"
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on post #{self.post_id}"

class Like(PrefixedIDModel):
    id_prefix = "rlk-"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} likes post #{self.post_id}"

#no table for shares and repost because we dont need to know who did

class CommentLike(PrefixedIDModel):
    id_prefix = "rclk-"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user.username} likes comment #{self.comment_id}"

class PostBoost(PrefixedIDModel):
    id_prefix = "rbst-"
    REACH_TIERS = [
        (500, "500 viewers - 10 pts"),
        (2000, "2,000 viewers - 30 pts"),
        (10000, "10,000 viewers - 100 pts"),
    ]

    ACTIVE = "active"
    EXPIRED = "expired"
    STATUS_CHOICES = [(ACTIVE, "Active"), (EXPIRED, "Expired")]

    post = models.OneToOneField(FeedPost, on_delete=models.CASCADE, related_name="boost")
    reach = models.PositiveIntegerField(choices=REACH_TIERS)
    points_cost = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boost of post #{self.post_id} ({self.reach} reach)"