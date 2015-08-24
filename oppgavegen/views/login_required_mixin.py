from django.contrib.auth.decorators import login_required, user_passes_test

class LoginRequiredMixin(object):
    """ Generic @login_required Mixin for class-based views  """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)