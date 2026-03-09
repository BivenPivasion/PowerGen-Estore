from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Feature, ProductFeatureValue

# --- INLINES ---

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; border-radius: 5px;">')
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"


class ProductFeatureValueInline(admin.TabularInline):
    model = ProductFeatureValue
    extra = 1
    autocomplete_fields = ['feature'] 


# --- ADMIN CLASSES ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'image_show']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['parent']

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover;">')
        return "-"
    image_show.short_description = "Фото"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_show', 'name', 'price', 'stock', 
        'available', 'is_featured', 'category', 'updated_at'
    ]
    list_filter = ['available', 'is_featured', 'category', 'created_at']
    list_editable = ['price', 'stock', 'available', 'is_featured'] 
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureValueInline, ProductImageInline]
    list_per_page = 20
    save_on_top = True 

    fieldsets = (
        ("Основне", {
            "fields": ("category", "name", "slug", "price")
        }),
        ("Статус та склад", {
            "fields": ("stock", "available", "is_featured"),
        }),
        ("Опис", {
            "fields": ("short_description", "description"),
            "classes": ("collapse",) 
        }),
    )

    def image_show(self, obj):
        # Використовуємо related_name='images' з вашої моделі ProductImage
        first_image = obj.images.first()
        if first_image and first_image.image: 
            return mark_safe(f'<img src="{first_image.image.url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;">')
        return "Немає фото"
    image_show.short_description = "Фото"


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    # Тут ми залишили тільки ті поля, які реально є в моделі Feature
    list_display = ['name', 'unit']
    search_fields = ['name']
    # Поля slug, price, stock немає в моделі Feature, тому ми їх видалили звідси,
    # щоб Django не видавав помилку при запуску.