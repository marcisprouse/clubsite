from django.contrib import admin
from .models import MyProfile
# from django.contrib.auth.models import User
from certificates.models import Certificate
from userena.utils import get_profile_model
from django.contrib.auth import get_user_model
from userena.admin import UserenaAdmin, UserenaSignupInline




class MyProfileAdmin(admin.ModelAdmin):
    list_per_page = 1000
    list_display = ["user", "member_id", "cell_phone", "other_phone", "is_active_member", "is_a_member_full_time_resident", "is_a_renter_member", "member_coyote_lakes_qualifying_address", "exclude_member_coyote_lakes_address_from_site", "is_a_member_part_time_resident", "member_part_time_away_address", "is_a_landlord_with_transferred_membership", "landlord_away_address", "is_other", "date_first_entered", "created", "updated"]
    search_fields = ["user__first_name","user__last_name", "member_coyote_lakes_qualifying_address__member_coyote_lakes_address__route", "member_coyote_lakes_qualifying_address__member_coyote_lakes_address__street_number", "member_coyote_lakes_qualifying_address__certificate_number"]
    ordering = ('-member_id',)

#docs from https://github.com/bread-and-pepper/django-userena/blob/master/docs/faq.rst
admin.site.unregister(get_profile_model())
admin.site.register(MyProfile, MyProfileAdmin)


class MyProfileAdminInline(admin.StackedInline):
    model = MyProfile
    list_per_page = 1000
    list_display = ["user", "member_id", "cell_phone", "other_phone", "is_active_member", "is_a_member_full_time_resident", "is_a_renter_member", "member_coyote_lakes_qualifying_address", "is_a_member_part_time_resident", "member_part_time_away_address", "is_a_landlord_with_transferred_membership", "landlord_away_address", "is_other", "member_notes", "date_first_entered", "created", "updated"]





class MyProfileAddedAdmin(UserenaAdmin):
    inlines = [UserenaSignupInline, MyProfileAdminInline]


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), MyProfileAddedAdmin)

