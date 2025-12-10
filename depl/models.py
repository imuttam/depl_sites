from django.db import models
# BA	OA	District	Village/Site	Village Code	Site ID	AT-3 Date	LOT 

class Site(models.Model):
    ba = models.CharField(max_length=20)
    oa = models.CharField(max_length=20)
    district = models.CharField(max_length=50)
    village_site = models.CharField(max_length=50)
    village_code = models.CharField(max_length=50, blank=True, null=True)
    site_id = models.CharField(max_length=50, unique=True)
    at3_date = models.DateField()
    lot = models.CharField(max_length=20)
    site_dev = models.BooleanField(default=False)

    def __str__(self):
        return self.village_site
