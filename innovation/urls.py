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


def rowcreate():
    ToolsAndInnovations.objects.all().delete()
    with open('Tools.csv') as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            print(row)
            if index <= 2:
                index += 1
                continue
            else:
                tools, created = ToolsAndInnovations.objects.get_or_create(
                    name=row[1],
                    url=row[2],
                    web_launchyear=row[4],
                    prime_phase_alpha=row[5],
                    prime_phase_number=row[6],
                    function_free=row[7],
                    ui_functionfree=row[8],
                    function_controlled=row[9],
                    geo_category=row[10],
                    ui_geo_category=row[11],
                    twitter=row[12],
                    twitter_follow_latest=row[14],
                    active_pre=row[15],
                    active_dis=row[16],
                    active_ana=row[17],
                    active_wri=row[18],
                    active_pub=row[19],
                    active_out=row[20],
                    active_ass=row[21],
                )
            index += 1