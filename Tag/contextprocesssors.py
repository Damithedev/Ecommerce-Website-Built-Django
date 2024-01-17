# context_processors.py
from base.forms import CustomUserCreationForm, CustomAuthenticationForm
from base.models import Category

def common_context(request):
    registration_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()
    all_categories = Category.objects.all()

    return {
        'registration_form': registration_form,
        'login_form': login_form,
        'all_categories': all_categories,
    }
