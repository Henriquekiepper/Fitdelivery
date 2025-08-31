from django.contrib import admin

from suplements.models import Brand, Category, Vendor, Supplement, SupplementInventory,Gym


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'created_at')
    search_fields = ('store_name', 'user__username')


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'vendor', 'price', 'stock_quantity', 'created_at')
    list_filter = ('brand', 'category', 'vendor')
    search_fields = ('name', 'brand__name', 'category__name', 'vendor__store_name')
    readonly_fields = ('created_at',)


@admin.register(SupplementInventory)
class SupplementInventoryAdmin(admin.ModelAdmin):
    list_display = ('total_products', 'total_value', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Gym) 
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)
