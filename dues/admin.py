from django.contrib import admin
from dues.models import Balance
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import IntegerWidget
from import_export.fields import Field


# Register your models here.
@admin.register(Balance)
class BalanceAdmin(ImportExportModelAdmin):
    list_per_page = 1000
    list_display = ("id", "cert", "balance", "created", "updated")
    search_fields = ["cert", "balance"]
    list_filter = ("balance", "updated")


class BalanceResource(resources.ModelResource):

    class Meta:
        model = Balance
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('cert')
        exclude = ('id',)
        fields = ('cert', 'balance')

    cert = Field(
        column_name = 'cert',
        attribute = 'cert',
        widget = IntegerWidget()
        )
