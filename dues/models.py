from django.db import models

# Create your models here.
class Balance(models.Model):
    cert = models.PositiveIntegerField('cert', null=True, blank=True)
    balance = models.CharField('balance', max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['cert']


    def __str__(self):
        return f"{self.cert} -- {self.balance}"
