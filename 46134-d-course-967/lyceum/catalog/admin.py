from django.contrib import admin

import catalog.models

__all__ = []


class ImageGalleryInline(admin.TabularInline):
    model = catalog.models.ItemImageGallery
    extra = 1


class MainImageInline(admin.TabularInline):
    model = catalog.models.ItemMainImage


@admin.register(catalog.models.ItemMainImage)
class MainAdmin(admin.ModelAdmin):
    list_display = (catalog.models.ItemMainImage.image_tmb,)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.ItemMainImage.preview,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = [catalog.models.Item.tags.field.name]

    readonly_fields = [catalog.models.ItemMainImage.preview]

    inlines = [
        MainImageInline,
        ImageGalleryInline,
    ]


admin.site.register(catalog.models.Category)
admin.site.register(catalog.models.Tag)
admin.site.register(catalog.models.ItemImageGallery)
