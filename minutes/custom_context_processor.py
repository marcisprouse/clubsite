from minutes.models import PostMinute
import random
from django.core.cache import cache


def post_minutes_renderer(request):
    cached = cache.get("ctx:minutes:post_minutes_renderer")
    if cached is not None:
        return cached

    all_posts = PostMinute.objects.all()
    pub_posts = PostMinute.objects.all().filter(status="published")
    all_posts_list = []
    palette = []

    for post in all_posts:
        all_posts_list.append(post)

    for p in all_posts_list:
        random_number = random.randint(0,16777215)
        hex_number =format(random_number,'x')
        hex_number = '#'+hex_number
        palette.append(hex_number)

    retval = {'all_posts':all_posts,
              'palette':palette,
              'pub_posts':pub_posts,
              'all_posts_list':all_posts_list
              }
    cache.set("ctx:minutes:post_minutes_renderer", retval, 120)
    return retval
