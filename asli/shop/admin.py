from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','is_sub')
    list_filter=('is_sub',)
    search_fields=('name',)
    prepopulated_fields={'slug':('name',)}

admin.site.register(Product)
admin.site.register(Select_IMG_Product)

# @admin.register(Order)
class OrderInlin(admin.TabularInline):
    model=OrderIten

class OrderAdmin(admin.ModelAdmin):
    inlines=(OrderInlin,)
admin.site.register(Order,OrderAdmin)


admin.site.register(Cupon)
admin.site.register(CommentProduct)
