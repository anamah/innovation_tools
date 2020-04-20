from material.frontend.views import ModelViewSet

from . import models

class OceanViewSet(ModelViewSet):
    model = models.Ocean
    list_display = ('name', 'area', 'map_url')


class StartDataViewSet(ModelViewSet):
    model = models.Startdata
    list_display  = [field.name for field in model._meta.fields]


class MetaDataViewSet(ModelViewSet):
    model = models.Metadata
    list_display = ('research_phase_number', 'research_phases30', 'research_phases7')


class ToolsAndInnovationsViewSet(ModelViewSet):
    model = models.ToolsAndInnovations
    list_display = [field.name for field in model._meta.fields]


class RecommendationViewSet(ModelViewSet):
    model = models.Recommendation
    list_display = ('creators_title', 'link')