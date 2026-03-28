from tables.models import Table
from tables.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class TableListView(OwnerListView):
    model = Table
    # By convention:
    # template_name = "myarts/article_list.html"


class TableDetailView(OwnerDetailView):
    model = Table


class TableCreateView(OwnerCreateView):
    model = Table
    fields = ['table_name', 'theme_description', 'picture',  'name_for_seat_one', 'name_for_seat_two', 'name_for_seat_three', 'name_for_seat_four', 'name_for_seat_five', 'name_for_seat_six', 'name_for_seat_seven', 'name_for_seat_eight']


class TableUpdateView(OwnerUpdateView):
    model = Table
    fields = ['table_name', 'theme_description', 'picture',  'name_for_seat_one', 'name_for_seat_two', 'name_for_seat_three', 'name_for_seat_four', 'name_for_seat_five', 'name_for_seat_six', 'name_for_seat_seven', 'name_for_seat_eight']


class TableDeleteView(OwnerDeleteView):
    model = Table
