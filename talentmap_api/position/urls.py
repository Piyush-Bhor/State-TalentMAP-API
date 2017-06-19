from django.conf.urls import url

from talentmap_api.position import views

get_list = {'get': 'list'}

urlpatterns = [
    url(r'^$', views.PositionListView.as_view(get_list), name='view-positions'),
]
