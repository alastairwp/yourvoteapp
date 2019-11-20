from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    landing_page = models.CharField(max_length=255, null=True, blank=True, name="landing_page")

    auto_create_schema = True
    auto_drop_schema = False


class Domain(DomainMixin):
    pass