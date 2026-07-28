from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend app (all main pages)
    path('', include('frontend.urls')),

    # Django built-in auth (login, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]
