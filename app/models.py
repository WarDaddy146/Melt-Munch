
from django.db import models  # This gives us tools to create database tables
from django.contrib.auth.models import User  # This brings in Django's built-in user system
from django.utils import timezone  # This helps us work with dates and times


class Product(models.Model):
    cat_ops = [
        ('Cookies', 'Cakes', 'Breads', 'Pastries', 'Chocolates', 'Celebrations'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, choices=[(cat, cat) for cat in cat_ops[0]], default='Cookies')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    def is_in_stock(self):
        return self.quantity > 0
    
    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'product')  # Prevents duplicate favorites
        
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Cart(models.Model):
    # This is our Cart blueprint - it describes what information each cart should have
    
    # The user who owns this cart
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The products in this cart
    # ManyToManyField means a cart can have many products, and a product can be in many carts
    products = models.ManyToManyField(Product)
    
    # The date and time when the cart was created
    created_at = models.DateTimeField(default=timezone.now)
    
    # This special method tells Django how to display the cart when we print it
    def __str__(self):
        return f"Cart of {self.user.username} with {self.products.count()} products"
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.quantity} of {self.product.name} for {self.user.username}"
    

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        if self.product.quantity < self.quantity:
            raise ValueError("Insufficient stock")
        self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)