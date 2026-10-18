from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0020_feature_rsvp_occurrence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Add information that is not already on the flyer. To make a link, use [text](full website address) with no space between the brackets and parentheses. For a direct RSVP link, select an RSVP occurrence below. To link to the general RSVP list instead, copy and paste: [RSVP Here](https://www.coyotelakesrecreationclub.org/activity/respond)",
                null=True,
            ),
        ),
    ]
