from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')



class Feature(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250, help_text="What is the title of your Featured activity?")
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', help_text="This field automatically populates as you type in the title. It's needed to distinguish it from other featured FLYERS.")
    description = models.TextField(blank=True, null=True, help_text="In your description, let everyone know details about the featured event that is not on the flyer. No need to put Date or Time as this will automatically appear. Indicate what members need to bring, if applies.  To make a link use this format: [text](full website address) NO SPACE BETWEEN BRACKETS AND PARENTHESIS - Example for reservation link: [RSVP Requested](https://www.coyotelakesrecreationclub.org/activity/respond). Example for Volunteer link: [Volunteers Needed](https://www.coyotelakesrecreationclub.org/activity/vol). Example for email contact: [Email Monica Hall](mailto:rlmhallmi@yahoo.com).  **text** will show up as bold type. A dash (-) before items in a list will format as a list.")
    feature_day_time = models.DateTimeField(default=timezone.now, help_text="This is the date/time of the actual activity...not the day you want it published")
    feature_location = models.CharField(max_length=250, blank=True, default=None, help_text="If you put something here, it will appear on the site. You can leave it blank if it's at the Club.")
    featured_flyer = models.FileField(upload_to='pages/images/feature', blank=True, null=True, help_text="Convert your .doc Flyer File to a .jpg. There are online tools to do this.  One of them is https://cloudconvert.com/docx-to-jpg")
    publish = models.DateTimeField(default=timezone.now, help_text="When do you want this flyer to appear on the site? If you are featuring more than one flyer on the homepage, the date that is closest to 'now' will appear first on the page.")
    expire = models.DateTimeField(default=timezone.now, help_text="Put in the day/time you would like for this feature FLYER to expire (no longer show up on the site).")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', help_text="If set to Draft, the feature FLYER will NEVER appear. If set to Published, the feature FLYER will appear between the set Publish and Expire dates.")

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:feature_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


class Alert(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    COLOR_CHOICES = (
        ('primary', 'Sky Blue'),
        ('secondary', 'Gray'),
        ('success', 'Green'),
        ('danger', 'Reddish-Pink'),
        ('warning', 'Yellow'),
        ('info', 'Light Blue'),
        ('light', 'White'),
        ('dark', 'Dark Gray')
    )
    title = models.CharField(max_length=250, help_text="You can say, 'Alert', 'Important', 'Important Pool Information', etc.")
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', help_text="This field automatically populates as you type in the title. It's needed to distinguish it from other alerts.")
    text = models.TextField(blank=True, null=True, help_text="Just enter text you want in the alert. To make a link use this format: [text](full website address) NO SPACE BETWEEN BRACKETS AND PARENTHESIS - Example for email contact: [Email Bill Ross](mailto:listmanager@cylrc.org).  **text** will show up as bold type.")
    publish = models.DateTimeField(default=timezone.now, help_text="When do you want the alert to appear? If you are featuring more than one Alert on the homepage, the date that is closest to 'now' will appear first on the page.")
    expire = models.DateTimeField(default=timezone.now, help_text="Put in the day/time you would like for this alert to expire (no longer show up on the site).")
    alert_color = models.CharField(max_length=10,
                              choices=COLOR_CHOICES,
                              default='danger', help_text="This is the color the box and fill around your alert will be.  It defaults to Reddish-Pink.")
    created = models.DateTimeField(auto_now_add=True, help_text="You don't need to do anything here. It's automatic.")
    updated = models.DateTimeField(auto_now=True, help_text="You don't need to do anything here. It's automatic.")
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', help_text="If set to Draft, the alert will NEVER appear. If set to Published, the alert will appear between the set Publish and Expire dates.")
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:alert_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


class ActivityBulletinBoard(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    COLOR_CHOICES = (
        ('primary', 'Sky Blue'),
        ('secondary', 'Gray'),
        ('success', 'Green'),
        ('danger', 'Reddish-Pink'),
        ('warning', 'Yellow'),
        ('info', 'Light Blue'),
        ('light', 'White'),
        ('dark', 'Dark Gray')
    )
    title = models.CharField(max_length=250, help_text="You can say, 'Leaders Required', 'Important', 'Yard Sale Help Needed', etc.")
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish', help_text="This field automatically populates as you type in the title of your pinned note. It's needed to distinguish it from other pinned notes.")
    text = models.TextField(blank=True, null=True, help_text="Just enter text you want in the pinned note. To make a link use this format: [text](full website address) NO SPACE BETWEEN BRACKETS AND PARENTHESIS - Example for email contact: [Email Monica Hall](mailto:rlmhall2@gmail.com).  **text** will show up as bold type.")
    publish = models.DateTimeField(default=timezone.now, help_text="When do you want the pinned note to appear? If you are featuring more than one pinned note on the activity page, the date that is closest to 'now' will appear first on the page.")
    expire = models.DateTimeField(default=timezone.now, help_text="Put in the day/time you would like for this pinned note to expire (no longer show up on the site).")
    paper_color = models.CharField(max_length=10,
                              choices=COLOR_CHOICES,
                              default='danger', help_text="This is the color of the paper your pinned note will be.  It defaults to Reddish-Pink.")
    created = models.DateTimeField(auto_now_add=True, help_text="You don't need to do anything here. It's automatic.")
    updated = models.DateTimeField(auto_now=True, help_text="You don't need to do anything here. It's automatic.")
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', help_text="If set to Draft, the pinned note will NEVER appear. If set to Published, the pinned note will appear between the set Publish and Expire dates.")
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:bulletin_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])




