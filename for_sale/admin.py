from django.contrib import admin
from for_sale.models import Sale

# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_per_page = 1000
    list_display = ("certificate_name", "date_resigned", "sold_to", "purchase_date", "for_sale_notes", "created", "updated")
    search_fields = ["certificate_name", "sold_to","for_sale_notes"]
    list_filter = ("date_resigned", "purchase_date")


