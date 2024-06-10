from django.contrib import admin # type: ignore
from .models import *
# Register your models here.

# class adminCart(admin.ModelAdmin):
#     list_display = ('user', 'productid', 'quantity','status')
#     sortable_by = ['user']
#     list_per_page = 10
#     list_max_show_all = 100
    
admin.site.register(FitUser)
admin.site.register(Diet)
admin.site.register(Workout)
admin.site.register(Feedback)
admin.site.register(Shop_Item)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(trainer)

