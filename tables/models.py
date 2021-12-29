from django.db import models
from accounts.models import MyProfile
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_only_thirteen_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 13 and
            obj.id != model.objects.get().id):
        raise ValidationError("Can only create 13 %s instance" % model.__name__)


# Create your models here.
class Table(models.Model) :
    def clean(self):
        validate_only_thirteen_instance(self)
    table_name = models.CharField(
          max_length=200,
          validators=[MinLengthValidator(2, "Title must be greater than 2 characters")], help_text='Name your table based on the theme'
    )
    theme_description = models.TextField(null=True, blank=True)
    picture = models.BinaryField(null=True, blank=True, editable=True, help_text='Add a picture of your table inspiration, if you like.')
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name_for_seat_one = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_two = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_three = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_four = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_five = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_six = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_seven = models.CharField(max_length=100, null=True, blank=True)
    name_for_seat_eight = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comms = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comm', related_name='comms_owned')

    # Shows up in the admin list
    def __str__(self):
      return self.table_name

class Comm(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
