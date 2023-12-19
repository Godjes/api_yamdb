from django.contrib import admin

from users.forms import AuthenticationForm
from users.models import User

admin.site.login_form = AuthenticationForm

admin.site.register(User)
