from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.detail import SingleObjectMixin
from django.contrib.sites.models import Site

class LoginRequiredMixin(object):
    """ Generic @login_required Mixin for class-based views  """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
