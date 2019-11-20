from customers.models import Client, Domain
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseNotFound


class MultiSiteMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.get_host())
        try:
            domain = request.get_host().split(":")[0]
            tenant = Domain.objects.get(domain=domain)
            client = Client.objects.get(id=tenant.id)
            request.site = client.landing_page
            print(request.site)
        except Client.DoesNotExist:
            print("not found")
            return HttpResponseNotFound()

