from django.urls import path
from .views import (
    SiteListView, SiteDetailView,
    SiteCreateView, SiteUpdateView,
    SiteDeleteView
)

urlpatterns = [
    path("", SiteListView.as_view(), name="site_list"),
    path("<int:pk>/", SiteDetailView.as_view(), name="site_detail"),
    path("create/", SiteCreateView.as_view(), name="site_create"),
    path("<int:pk>/edit/", SiteUpdateView.as_view(), name="site_edit"),
    path("<int:pk>/delete/", SiteDeleteView.as_view(), name="site_delete"),
]
