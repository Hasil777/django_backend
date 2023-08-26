from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True,
                                null=True,)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()


class Product(models.Model):
    user = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True,
                             null=True,)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product/%Y/%m/%d', default='',
                              blank=True,
                              null=True)
    brand = models.CharField(max_length=50)
    category = models.ForeignKey(Category, models.SET_NULL, blank=True,
                                 null=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100)

    def __str__(self) -> str:
        return self.name

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Product, self).save()

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-createdAt']),
        ]


class Review(models.Model):
    product = models.ForeignKey(Product, models.SET_NULL, blank=True,
                                null=True)
    user = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True,
                             null=True,)
    name = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=7, decimal_places=2)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]


class Order(models.Model):
    user = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True,
                             null=True,)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, blank=True,
                                   null=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2,
                                        blank=True, null=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2,
                                     blank=True, null=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    isDeliveredAt = models.DateTimeField(auto_now_add=False,
                                         blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    product = models.ForeignKey(Product, models.SET_NULL,
                                blank=True, null=True)

    class Meta:
        ordering = ['createdAt']
        indexes = [
            models.Index(fields=['createdAt']),
        ]

    def __str__(self) -> str:
        return self.product.name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, models.SET_NULL,
                                blank=True, null=True)
    order = models.ForeignKey(Order, models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                blank=True, null=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d',
                              blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 blank=True, null=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2,
                                        blank=True, null=True)

    def __str__(self) -> str:
        return self.order.product.name
