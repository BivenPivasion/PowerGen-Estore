from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(unique=True, verbose_name="URL слаг")
    image = models.ImageField(upload_to='category/', blank=True, null=True, verbose_name="Зображення")
    
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='children', verbose_name='Батьківська категорія'
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


    def get_descendants(self, include_self=True):
        """
        Повертає QuerySet усіх нащадків. 
        Використовуємо ID, щоб уникнути проблем з поєднанням різних QuerySet.
        """
        # Створюємо список ID, починаючи з поточного об'єкта
        descendant_ids = [self.pk] if include_self else []
        
        # Функція для рекурсивного збору ID
        def collect_ids(category):
            for child in category.children.all():
                descendant_ids.append(child.pk)
                collect_ids(child)
        
        collect_ids(self)
        
        # Повертаємо один чистий QuerySet
        return Category.objects.filter(pk__in=descendant_ids)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, 
        null=True, verbose_name="Категорія"
    ) 
    name = models.CharField(max_length=200, verbose_name="Назва продукту")
    slug = models.SlugField(unique=True, verbose_name="URL слаг")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    
    short_description = models.CharField(max_length=255, verbose_name="Короткий опис")
    description = models.TextField(verbose_name="Повний опис", blank=True)
    
    stock = models.PositiveIntegerField(default=0, verbose_name="Залишок на складі")
    available = models.BooleanField(default=True, verbose_name="Доступний до замовлення")
    is_featured = models.BooleanField(default=False, verbose_name="Обраний товар")
# null должен забраться
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at', 'name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
    
    @property
    def main_image(self):
        img = self.images.first()
        if img:
            return img.image.url
        return '/static/img/no_image.png'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")
   # null должен забраться
    image = models.ImageField(null=True, blank=True, upload_to='products/', verbose_name="Зображення")
    
    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Зображення товарів"

    def __str__(self):
        return f"Image for {self.product.name}"


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва характеристики")
    unit = models.CharField(max_length=50, blank=True, verbose_name="Од. виміру", help_text="напр. кВт, л, мм")
    
    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name


class ProductFeatureValue(models.Model):
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name="Характеристика")
    value = models.CharField(max_length=255, verbose_name="Значення") 
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")

    class Meta:
        unique_together = ('product', 'feature')
        ordering = ['order']
        verbose_name = "Значення характеристики"
        verbose_name_plural = "Значення характеристик"
        
    def __str__(self):
        return f"{self.product.name}: {self.feature.name} - {self.value}"