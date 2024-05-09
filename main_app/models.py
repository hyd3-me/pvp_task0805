from django.db import models
from django.contrib.auth.models import User

import uuid


# Create your models here.

class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_buy = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ref_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refr')
    referral = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refl')
    date_joined = models.DateTimeField(auto_now_add=True)
    num_purchases = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0.0)

    def __str__(self):
        return f'refs {self.referrer} >> {self.referral}'

class RefBuyer(Buyer):
    referral_obj = models.ForeignKey(Referral, on_delete=models.CASCADE)