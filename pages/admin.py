from django.contrib import admin
from .models import Feature, Alert, ActivityBulletinBoard

# Register your models here.
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'feature_day_time', 'feature_location', 'featured_flyer', 'publish', 'expire', 'created', 'updated', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'publish', 'expire', 'alert_color', 'created', 'updated', 'status')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ActivityBulletinBoard)
class ActivityBulletinBoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'publish', 'expire', 'paper_color', 'created', 'updated', 'status')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}