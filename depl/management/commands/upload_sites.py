import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from depl.models import Site


class Command(BaseCommand):
    help = "Upload Site data from CSV file"

    def parse_date(self, date_str):
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

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to CSV file")

    def handle(self, *args, **options):
        

        file_path = options['csv_file']

        with open(file_path, 'r', encoding='utf-8-sig') as f:   # note utf-8-sig
            reader = csv.reader(f)
            rows = list(reader)

            # clean header
            header = [h.strip() for h in rows[0]]
            data_rows = rows[1:]

            # create dict-reader manually
            cleaned_rows = []
            for row in data_rows:
                cleaned_rows.append({header[i]: row[i].strip() for i in range(len(header))})

            count = 0

            for row in cleaned_rows:
                try:
                    # at3_date = datetime.strptime(row['AT-3 Date'], "%d-%b-%y").date() 
                    at3_date = self.parse_date(row['AT-3 Date'])

                    Site.objects.update_or_create(
                        site_id=row['Site ID'],
                        defaults={
                            "ba": row['BA'],
                            "oa": row['OA'],
                            "district": row['District'],
                            "village_site": row['Village/Site'],
                            "village_code": row.get('Village Code') or None,
                            "at3_date": at3_date,
                            "lot": row['LOT'],  # now this will always work
                        }
                    )

                    count += 1

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Error at Site ID {row.get('Site ID')}: {e}"
                    ))

            self.stdout.write(self.style.SUCCESS(f"Uploaded {count} records successfully"))
