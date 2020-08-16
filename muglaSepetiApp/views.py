from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from muglaSepetiApp.models import Bucket


def test(request):
    page_url = "assets/index.html"
    return render(request, template_name=page_url)


def check(request, pk):
    Bucket.objects.get(pk=pk).check_order()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def ontheway(request, pk):
    Bucket.objects.get(pk=pk).order_on_the_way()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deliver(request, pk):
    Bucket.objects.get(pk=pk).deliver_order()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cancel(request, pk):
    Bucket.objects.get(pk=pk).cancel_order()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_more_tables(request):
    increment = int(request.GET['append_increment'])
    increment_to = increment + 10
    qs = Bucket.objects.all()
    if request.user.is_superuser:
        return render(request, 'get_more_data.html', {'order': qs})
    return render(request, 'get_more_data.html', {'order': qs.filter(company__owner=request.user, is_ordered=True)})
