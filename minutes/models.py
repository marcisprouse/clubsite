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
    video_title = models.CharField(max_length=30, blank=True, null=True)
    video_url_link = models.URLField(max_length=300, null=True, blank=True, help_text="Use this to provide a link to a video of the meeting that resides elsewhere (Such as Google Drive). Use complete url (e.g. https://drive.google.com/file/d/1RsePz_IBDLr_vajMBzo_h_6yhQUtdfRW/view?usp=sharing")
    audio_recording=models.FileField(blank=True, null=True, upload_to='minutes/audio/', help_text="Max file size: 100MB. Please upload audio recording in .mp3 or .m4a format. If you need another format, please let Marci know.")
    video_recording=models.FileField(blank=True, null=True, upload_to='minutes/video/', help_text="Max file size: 100MB. Please upload video recording in .mp4 format. If you need another format, please let Marci know.")
    pdf=models.FileField(blank=True, null=True, upload_to='minutes/pdf/', help_text="please upload .pdf file of meeting minutes.")
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
