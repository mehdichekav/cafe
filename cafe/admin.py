from django.contrib import admin
from .models import Table, MenuItems, Orders, Receipts, Category
# Register your models here.


admin.site.register(Table)

admin.site.register(Orders)
admin.site.register(Receipts)
admin.site.register(Category)

class MenuItemAdmin(admin.ModelAdmin):
    readonly_fields = ('create_timestamp','modify_timestamp',)

admin.site.register(MenuItems, MenuItemAdmin)