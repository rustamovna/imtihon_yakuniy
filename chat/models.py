from django.db import models
from django.contrib.auth.models import User
from ads.models import Ad

class MessageThread(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='threads')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_threads')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_threads')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ad', 'buyer')  

    def __str__(self):
        return f"{self.ad.title} - {self.buyer.username} ↔ {self.seller.username}"



class Message(models.Model):
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"