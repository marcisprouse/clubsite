from django.urls import path

from .views import AddMembersToExistingHouseholdView, NewMemberHouseholdView

app_name = "memberadmin"

urlpatterns = [
    path("", NewMemberHouseholdView.as_view(), name="new_member_household"),
    path(
        "existing-household/",
        AddMembersToExistingHouseholdView.as_view(),
        name="add_members_to_existing_household",
    ),
]

