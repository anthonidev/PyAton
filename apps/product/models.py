from datetime import datetime
from django.db import models
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify


class Brand(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    photo = CloudinaryField('Image', overwrite=True,
                            format="webp", blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_total(self):
        return Product.objects.filter(category=self).count()

    def get_absolute_url(self):
        return '/%s/' % (self.slug)

    def get_parent(self):
        return self.parent.title

    def get_parent_slug(self):
        return self.parent.slug

    def save(self, *args, **kwargs):
        to_assign = slugify(self.title)
        if Category.objects.filter(slug=to_assign).exists():
            to_assign = to_assign+str(Category.objects.all().count())
        self.slug = to_assign
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='categories', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    parent = models.ForeignKey(
        'self', related_name='colors', on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    compare_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    sold = models.IntegerField(default=0)
    photo = CloudinaryField('Image', overwrite=True, format="webp")
    photo_thumbnail_sm = CloudinaryField(
        'photo_thumbnail_sm', overwrite=True, format="webp", blank=True, null=True)
    photo_thumbnail_xm = CloudinaryField(
        'photo_thumbnail_xm', overwrite=True, format="webp", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-date_added',)

    def save(self, *args, **kwargs):
        if not self.id:
            to_assign = slugify(self.title)
            if Product.objects.filter(slug=to_assign).exists():
                to_assign = to_assign+str(Product.objects.all().count())
            self.slug = to_assign
            super().save(*args, **kwargs)

    def get_colors(self):
        if (self.parent):
            id = []
            for p in Product.objects.all().filter(parent=self.parent):
                id.append(p.id)
            id.append(self.parent.id)
            return Product.objects.all().filter(id__in=id).exclude(id=self.id)
        else:
            products = Product.objects.filter(parent=self).exclude(id=self.id)
            return products

    def related_products(self):
        return Product.objects.filter(category=self.category).exclude(id=self.id)[:4]

    def get_category(self):
        return self.category.title

    def get_brand(self):
        return self.brand.title

    def __str__(self):
        return self.title


class CharacteristicProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='characteristics')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    photo = CloudinaryField('Image', overwrite=True, format="jpg")
    photo_thumbnail_sm = CloudinaryField(
        'photo_thumbnail_sm', overwrite=True, format="webp", blank=True, null=True)
    photo_thumbnail_xm = CloudinaryField(
        'photo_thumbnail_xm', overwrite=True, format="webp", blank=True, null=True)

    def __str__(self):
        return self.product.title
