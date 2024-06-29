"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

history_urls = [
    path("history/", include("history.urls")),
    path("history/schema/", SpectacularAPIView.as_view(), name="history_schema"),
    path(
        "history/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="history_schema"),
        name="history_swagger",
    ),
]

# URLs for the first API (auth)
auth_urls = [
    path("myauth/", include("myauthapi.urls")),
    path("myauth/schema/", SpectacularAPIView.as_view(), name="auth_schema"),
    path(
        "myauth/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="auth_schema"),
        name="auth_swagger",
    ),
]

# URLs for the second API (bicycles)
bicycle_urls = [
    path("bicycles/", include("bicycleapi.urls")),
    path("bicycles/schema/", SpectacularAPIView.as_view(), name="bicycle_schema"),
    path(
        "bicycles/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="bicycle_schema"),
        name="bicycle_swagger",
    ),
]

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    *auth_urls,
    *bicycle_urls,
    *history_urls,
]
