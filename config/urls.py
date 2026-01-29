from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', include('inventory.urls')),
    path('', RedirectView.as_view(url='/items/', permanent=True)),
]