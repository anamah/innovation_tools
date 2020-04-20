from django.conf.urls import url, include
from django.views import generic

from . import views

urlpatterns = [
    url('^$', generic.RedirectView.as_view(url='./ocean/'), name="index"),
    url('^ocean/', include(views.OceanViewSet().urls)),
    url('^metadata/', include(views.MetaDataViewSet().urls)),
    url('^startdata/', include(views.StartDataViewSet().urls)),
    url('^information/', include(views.ToolsAndInnovationsViewSet().urls)),
    url('^reccomendation/', include(views.RecommendationViewSet().urls), name='reccomendation'),
]


