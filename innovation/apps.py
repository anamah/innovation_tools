from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class InnovationConfig(ModuleMixin, AppConfig):
    name = 'innovation'
    icon = '<i class="material-icons">settings_applications</i>'
    verbose_name = "CRUD sample"