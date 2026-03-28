from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime

# from django.core.files.uploadedfile import InMemoryUploadedFile

from tables.owner import OwnerListView, OwnerDetailView, OwnerDeleteView

from tables.models import Table, Comm
from tables.forms import CreateForm, CommForm

from tables.utils import dump_queries

from django.db.models import Q


class TableListView(OwnerListView):
    model = Table
    template_name = "tables/table_list.html"

    # Code for the favorites

    def get(self, request) :
        table_list = Table.objects.all()
        objects = Table.objects.all().order_by('-updated_at')[:10]
        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'table_list': objects}
        retval = render(request, self.template_name, ctx)

        # dump_queries()
        return retval;


class TableDetailView(OwnerDetailView):
    model = Table, Comm
    template_name = "tables/table_detail.html"
    def get(self, request, pk) :
        x = Table.objects.get(id=pk)
        comms = Comm.objects.filter(table=x).order_by('-updated_at')
        comm_form = CommForm()
        context = { 'table' : x, 'comms': comms, 'comm_form': comm_form }
        return render(request, self.template_name, context)


class TableCreateView(LoginRequiredMixin, View):
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:all_tables')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)

class CommCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Table, id=pk)
        comm = Comm(text=request.POST['comm'], owner=request.user, table=a)
        comm.save()
        return redirect(reverse('tables:table_detail', args=[pk]))

class TableUpdateView(LoginRequiredMixin, View):
    template_name = 'tables/table_form.html'
    success_url = reverse_lazy('tables:all_tables')

    def get(self, request, pk):
        pic = get_object_or_404(Table, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Table, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()

        return redirect(self.success_url)


class TableDeleteView(OwnerDeleteView):
    model = Table
    template_name = "tables/table_confirm_delete.html"

class CommDeleteView(OwnerDeleteView):
    model = Comm
    template_name = "tables/table_comm_delete.html"
    def get_success_url(self):
        table = self.object.table
        return reverse('tables:table_detail', args=[table.id])

def stream_file(request, pk):
    pic = get_object_or_404(Table, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
