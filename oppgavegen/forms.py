from django.forms import ModelForm
from .models import Set
from .models import Level
from .models import Template

class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ('name', 'chapter')

class Level(ModelForm):
    class Meta:
        model = Level
        fields = ('name', 'template')