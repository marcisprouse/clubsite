from django.contrib import admin
from keys.models import Key

# Register your models here.
@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_per_page = 1000
    list_display = ("certificate_and_qualifying_address_for_keys", "key_number_one", "key_number_two")
    search_fields = ["key_number_one", "key_number_two"]