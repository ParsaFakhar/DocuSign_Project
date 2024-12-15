from django.db import models
from django.contrib.auth.models import User


class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_email = models.EmailField()
    contract_id = models.CharField(max_length=100, null=True, blank=True)  # Store DocuSign envelope ID
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Draft")  # Draft, Signed, Completed


class TokenStorage(models.Model):
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refresh Token (Created: {self.created_at})"
