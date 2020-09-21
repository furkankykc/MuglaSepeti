from muglaSepetiApp.models import SiteConfig


def site_config(request):
    return {'config': SiteConfig.objects.first().config}
