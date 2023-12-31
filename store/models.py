from django.contrib import admin
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from uuid import uuid4
from .validators import validate_file_size
"""
Collection - Product  collection have multiple products

Customer - Order customer can have multiple order
Order - Item  order can have multiple items 
Cart - Item  cart can have multiple items as well
"""


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # products

    def __str__(self):
        return self.description


class Collection(models.Model):
    title = models.CharField(max_length=225)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)

    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['last_update',]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='store/images',
        validators=[validate_file_size]
    )
    """
    when we use FileField we can use File extension validator like this , imported from 'django.core.validators' 
    validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    """


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'

    # we use those function below because in AdminCustomer [list_display] we doesn't support 'user__first_name'
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        # db_table = 'store_customers'
        # indexes = [
        #     models.Index(fields=['last_name', 'first_name'])
        # ]
        ordering = ['user__last_name', 'user__first_name']
        permissions = [
            ('view_history', ('Can view history'))
        ]


class Address(models.Model):
    street = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    zip = models.DecimalField(decimal_places=0, max_digits=6)
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True)


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return f'order_{self.customer.first_name}_{self.customer.last_name}'

    # create custom permission
    class Meta:
        permissions = [
            ('cancel_order', 'Can Cancel Order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    # for no duplicated products we use unique_together on Meta class

    # class Meta:
    #     unique_together = [['cart', 'product'], []]
