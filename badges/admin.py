from django.contrib import admin
from badges.models import Badge

# Register your models here.
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("get_print_group", "print_date")
    # list_filter = ("issue_date")
