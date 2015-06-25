from oppgavegen.models import Template
from selectable.base import ModelLookup
from selectable.registry import registry


class TemplateLookup(ModelLookup):
    model = Template
    search_fields = ('tags__name__icontains')

registry.register(TemplateLookup)