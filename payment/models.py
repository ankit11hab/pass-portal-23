from django.db import models

# Create your models here.
class Payment(models.Model):
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField(default = 0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_id