from django.contrib import admin
from website.models import Product   # make sure you import your model
from website.models import AuthUser

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'price', 'description')

# Register the model with the custom admin
admin.site.register(Product, ProductAdmin)
admin.site.register(AuthUser)