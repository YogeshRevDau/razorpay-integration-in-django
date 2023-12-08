from django.db import models


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=400, blank=True)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_id}'
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_id = models.CharField(max_length=100, blank=True)
    reason = models.TextField()

    def __str__(self):
        return f'{self.order.name}----{self.order.order_id}'
