from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedManagerMinutes(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class PostMinute(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(help_text = "Please use this format: 'Month Date Year Board Meeting'. NO COMMA, PLEASE", max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', help_text = "This field automatically populates as you type the title.  Should look like this example: august-8-2021-board-meeting.")
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='minutes_posts', help_text = "Click on the magnifying glass and choose from that list." )
    attendance = models.TextField(help_text = "Example: Board members present: John Smith, Mary Jones, Jane Doe.  Approximately 30 members present.", blank=True)
    body = models.TextField(help_text = "Include only the body of the minutes (without the list of attendees and date).  To make a link use this format: [text](full website address) **text** will show up as bold type. A dash (-) before items in a list will format as a list.")
    publish = models.DateTimeField(default=timezone.now, help_text = "Enter the date that the meeting occured.  Time should be 06:00 am")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', help_text = "Select 'Published' for it to appear on the web site.")

    objects = models.Manager() # The default manager.
    published = PublishedManagerMinutes() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('minutes:post_minutes_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])
