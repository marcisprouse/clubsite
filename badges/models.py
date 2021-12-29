from django.db import models
from accounts.models import MyProfile

# Create your models here.

class Badge(models.Model):
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('yellow', 'Yellow'),
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('purple', 'Purple'),
        ('white', 'No Color')
    )
    members = models.ManyToManyField(MyProfile)
    print_date = models.DateField()
    badge_color = models.CharField(max_length=10,
                              choices=COLOR_CHOICES,
                              default='blue')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_print_group(self):
        return "\n".join([p.user.username for p in self.members.all()])