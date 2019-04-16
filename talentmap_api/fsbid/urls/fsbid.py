from django.conf.urls import url
from rest_framework import routers

from talentmap_api.fsbid.views import bidlist as views

router = routers.SimpleRouter()
# router.register(r'', views.FSBidListView, base_name="fsbid.FSBidList")

urlpatterns = [
    url(r'^position/(?P<pk>[0-9]+)/$', views.FSBidListPositionActionView.as_view(), name='bidding.FSBid-position-actions'),
    url(r'', views.FSBidListView.as_view(), name="bidding-FSBid-bid-actions"),
]

urlpatterns += router.urls
