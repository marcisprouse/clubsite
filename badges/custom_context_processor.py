from badges.models import Badge
from datetime import timedelta
from django.utils import timezone



def badge_renderer(request):
    all_badges = Badge.objects.all()

    all_badges_list=[]


    now = timezone.now()

    for badge in all_badges:
        past = badge.updated - timedelta(seconds=30)
        future = badge.updated + timedelta(seconds=30)

        if past <= now and now <= future:
            all_badges_list.append(badge)


    retval = {'all_badges':all_badges,
              'all_badges_list':all_badges_list
              }
    return retval;