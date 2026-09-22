from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.urls import reverse
from jsonfield import JSONField

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_restaurant = models.BooleanField(default=False)
    is_delivery = models.BooleanField(default=False)
    

class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    reg_num = models.CharField(max_length=200)
    res_name = models.CharField(max_length=200)
    owner = models.CharField(max_length=60)
    mobile = PhoneNumberField()
    addresses = models.CharField(max_length=2000, default='')
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pin = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.res_name

class Customer(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    cus_name=models.CharField(max_length=100)
    mobile = PhoneNumberField()

    def __str__(self):
        return self.cus_name


class Fishlist(models.Model):
    WEIGHT_CHOICES = (
        (1000, '1 kg'),
        (250, '250 grams'),
        (500, '500 grams'),
        (750, '750 grams'),
    )
    
    restaurant_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fish_name = models.CharField(max_length=30)
    description = models.CharField(max_length=350)
    rating = models.IntegerField(null=True)
    fish_image = models.ImageField(upload_to='images/')
    price = models.IntegerField()
    weight = models.PositiveIntegerField(choices=WEIGHT_CHOICES, default=1000)
    sold_out = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    main_product = models.BooleanField(default=False)
    def __str__(self):
        return self.fish_name

    def get_absolute_url(self):
        return reverse('updatefood', kwargs={'pk': self.pk})


class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay'),
    ]
    order_id = models.CharField(max_length=100)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.JSONField()
    payment_method = models.CharField(max_length=20, default=PAYMENT_METHOD_CHOICES)
    shipping_info = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    def get_scaled_price(self):
        return (self.fish_item.price * self.weight / 1000) * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts',default=None)
    fish_item = models.ForeignKey(Fishlist, on_delete=models.CASCADE, related_name='cart_items',default=None)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=1000)  # Store weight in grams

    def __str__(self):
        return f"{self.fish_item.fish_name} ({self.weight} grams) x {self.quantity}"
