from django.urls import path

from .views import NewMemberHouseholdView

app_name = "memberadmin"

urlpatterns = [
    path("", NewMemberHouseholdView.as_view(), name="new_member_household"),
]

