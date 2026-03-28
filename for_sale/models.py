from django.db import models


class Sale(models.Model):
    certificate_name = models.CharField(max_length=100, blank=True, null=True, help_text="Enter the certificate name (usually person or entity who is selling it).")
    date_resigned = models.DateField(default="", null=True, blank=True, help_text="Enter date of the certificate resignation. Format: YYYY-MM-DD")
    sold_to = models.CharField(max_length=100, blank=True, null=True, help_text="Enter the name of the person or entity the certificate was sold to. If there is no name in this blank, the certificate will appear in the for sale table on the website. Format: YYYY-MM-DD.")
    purchase_date = models.DateField(default="", null=True, blank=True, help_text="Enter date the certificate/membership was sold.")
    for_sale_notes = models.TextField(null=True, blank=True, help_text="These notes will NOT appear in the table. They only appear in the admin panel.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['date_resigned']


    def __str__(self):
        return u"Cert #: %s ---  %s" % (self.certificate_name, self.date_resigned)

