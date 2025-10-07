from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# -----------------
# Product Model
# -----------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    # image = models.ImageField(upload_to="products/", blank=True, null=True)  # Removed

    def __str__(self):
        return self.name


# -----------------
# Custom User Model
# -----------------
class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    # Removing unused fields
    user_permissions = None
    groups = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.username


# -----------------
# Cart Models
# -----------------
class Cart(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# -----------------
# Token Auto-Creation for Custom User
# -----------------
@receiver(post_save, sender=AuthUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        from rest_framework.authtoken.models import Token
        Token.objects.create(user=instance)
