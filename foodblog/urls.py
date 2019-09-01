from django.conf.urls import url
from . import views
urlpatterns = [
# food_list view as a function
url(r'^$',
views.food_list,
name='food_list'
),
# food_detail view as a function
url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
r'(?P<food>[-\w]+)/$',
views.food_detail,
name='food_detail'
),
url(r'^(?P<food_id>\d+)/share/$',
views.food_share,
name='food_share'),
]
