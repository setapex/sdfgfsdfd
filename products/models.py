from django.db import models
from multiselectfield import MultiSelectField


class Product(models.Model):
    SIZE_CHOICES = (('S', 'S'),
                    ('M', 'M'),
                    ('L', 'L'),
                    ('XL', 'XL'))

    sizes = MultiSelectField(choices=SIZE_CHOICES,
                             max_choices=6,
                             max_length=17)
    name = models.CharField(max_length=255, verbose_name='product_name')
    code = models.CharField(max_length=255, verbose_name='product_code')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=255, blank=True, null=True)
    image1_url = models.URLField(blank=True, null=True)
    image2_url = models.URLField(blank=True, null=True)
    image3_url = models.URLField(blank=True, null=True)
    image4_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, verbose_name='product_category')
    gender = models.CharField(max_length=255, verbose_name='product_gender')
    color = models.CharField(max_length=25, verbose_name='product_color')
    brand = models.CharField(max_length=25, verbose_name='product_brand')
    material = models.CharField(max_length=255, verbose_name='product_material')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}, Quantity: {self.quantity}"
