from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django_renderpdf.views import PDFView
# from django.views import View
from accounts.models import MyProfile


class ContactPDFView(LoginRequiredMixin, PDFView):
    """Generate labels for some Shipments.

    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'userena/contact_pdf.html'
    download_name = 'contacts.pdf'


    def get_context_data(request):
        """Pass some extra context to the template."""


        all_members = MyProfile.objects.all().order_by('user__last_name')
        all_members_list=[]

        for member in all_members:
            all_members_list.append(member)


        context = {'request':request,
                  'all_members':all_members,
                  'all_members_list':all_members_list,

                  }

        return context;



