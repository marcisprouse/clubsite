from django import forms
from tables.models import Table
from django.core.files.uploadedfile import InMemoryUploadedFile
from tables.humanize import naturalsize


# Create the form class.
class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'
    guest_one = forms.ChoiceField
    guest_two = forms.ChoiceField
    guest_three = forms.ChoiceField
    guest_four = forms.ChoiceField
    guest_five = forms.ChoiceField
    guest_six = forms.ChoiceField
    guest_seven = forms.ChoiceField

    # Hint: this will need to be changed for use in the ads application :)
    class Meta:
        model = Table
        fields = ['table_name', 'theme_description', 'picture', 'name_for_seat_one', 'name_for_seat_two', 'name_for_seat_three', 'name_for_seat_four', 'name_for_seat_five', 'name_for_seat_six', 'name_for_seat_seven', 'name_for_seat_eight']  # Picture is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance

class CommForm(forms.Form):
    comm = forms.CharField(required=True, max_length=500, min_length=3, strip=True)


# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
