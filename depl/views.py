from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
               ListView, DetailView,
              CreateView, UpdateView, DeleteView
                             )
from .models import Site
from django.db.models import Q


class SiteListView(ListView):
    model = Site
    template_name = "depl/site_list.html"
    context_object_name = "sites"
    paginate_by = 20

    # def get_queryset(self):
    #     qs = super().get_queryset()

    #     search = self.request.GET.get("q")
    #     if search:
    #         qs = qs.filter(village_site__icontains=search)

    #     return qs.order_by("district", "village_site")

    def get_queryset(self):
        qs = super().get_queryset()

        # Search text
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(
                Q(village_site__icontains=search) |
                Q(district__icontains=search)
            )

        # District filter (dropdown)
        district = self.request.GET.get("district")
        if district and district != "":
            qs = qs.filter(district=district)

        return qs.order_by("district", "village_site")


class SiteDetailView(DetailView):
    model = Site
    template_name = "depl/site_detail.html"
    context_object_name = "site"


class SiteCreateView(CreateView):
    model = Site
    fields = [
        "ba", "oa", "district", "village_site",
        "village_code", "site_id", "at3_date",
        "lot", "site_dev"
    ]
    template_name = "depl/site_form.html"
    success_url = reverse_lazy("site_list")


class SiteUpdateView(UpdateView):
    model = Site
    fields = [
        "ba", "oa", "district", "village_site",
        "village_code", "site_id", "at3_date",
        "lot", "site_dev"
    ]
    template_name = "depl/site_form.html"
    success_url = reverse_lazy("site_list")


class SiteDeleteView(DeleteView):
    model = Site
    template_name = "depl/site_confirm_delete.html"
    success_url = reverse_lazy("site_list")
