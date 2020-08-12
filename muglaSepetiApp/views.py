from django.shortcuts import render


# Create your views here.


def test(request):
    page_url = "assets/index.html"
    return render(request, template_name=page_url)
