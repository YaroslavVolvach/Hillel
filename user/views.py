from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class RegistrationView(generic.CreateView):
    form_class = CustomUserCreationForm
    model = User
    success_url = reverse_lazy('user_app:login')
    template_name = 'user/registration.html'

    def form_invalid(self, form):
        message = password_validation.password_validators_help_text_html()
        return self.render_to_response(self.get_context_data(form=form, message=message))
