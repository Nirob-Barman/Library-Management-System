from django.contrib import admin
from . models import UserLibraryAccount, UserAddress
# Register your models here.

class UserLibraryAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number','birthdate', 'gender', 'initial_deposit_date', 'balance')
    search_fields = ['user__username', 'account_number']


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'postal_code', 'country')
    search_fields = ['user__username', 'street_address',
                     'city', 'postal_code', 'country']


admin.site.register(UserLibraryAccount, UserLibraryAccountAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
