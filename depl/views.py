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



## UPLOAD DATA
import csv
from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from depl.models import Site


def parse_date(date_str):
    date_str = date_str.strip()

    formats = [
        "%d-%b-%y",   # 15-Feb-24
        "%d.%m.%y",   # 8.5.24
        "%d-%m-%y",   # 8-5-24
        "%d/%m/%y",   # 8/5/24
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Unknown date format: {date_str}")


def upload_csv(request):
    if request.method == "POST" and request.FILES.get("file"):

        csv_file = request.FILES["file"]
        decoded = csv_file.read().decode("utf-8-sig").splitlines()
        reader = csv.reader(decoded)

        rows = list(reader)
        header = [h.strip() for h in rows[0]]
        data_rows = rows[1:]

        # convert to list of dicts
        cleaned_rows = []
        for row in data_rows:
            cleaned_rows.append({header[i]: row[i].strip() for i in range(len(header))})

        count = 0
        errors = []

        with transaction.atomic():
            for row in cleaned_rows:
                try:
                    at3_date = parse_date(row['AT-3 Date'])

                    Site.objects.update_or_create(
                        site_id=row['Site ID'],
                        defaults={
                            "ba": row['BA'],
                            "oa": row['OA'],
                            "district": row['District'],
                            "village_site": row['Village/Site'],
                            "village_code": row.get('Village Code') or None,
                            "at3_date": at3_date,
                            "lot": row['LOT'],
                        }
                    )

                    count += 1

                except Exception as e:
                    errors.append(f"Error at Site ID {row.get('Site ID')}: {e}")

        return render(request, "upload_done.html", {
            "count": count,
            "errors": errors,
        })

    return render(request, "upload_form.html")
