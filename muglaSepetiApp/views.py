from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from muglaSepetiApp.models import Bucket, Company, Menu, Entry, FoodCategory


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


# not used only for example
def get_more_tables(request):
    increment = int(request.GET['append_increment'])
    increment_to = increment + 10
    qs = Bucket.objects.all()
    if request.user.is_superuser:
        return render(request, 'get_more_data.html', {'order': qs})
    return render(request, 'get_more_data.html', {'order': qs.filter(company__owner=request.user, is_ordered=True)})


def one_page_companies(request, company_id=0):
    open_companies = Company.get_open_companies()
    active_menu_ids = open_companies.values('active_menu')
    active_menus = Menu.objects.filter(id__in=active_menu_ids)
    active_menus = active_menus.all() if company_id == 0 else active_menus.filter(company_id=company_id)
    active_menus_entry_ids = active_menus.values_list('entry_list', flat=True)
    entries = Entry.objects.filter(id__in=active_menus_entry_ids)
    context = {
        'companies': open_companies,
        'menu': active_menus,
    }


def company_menu(request, cmp_slug):
    company = Company.objects.get(slug=cmp_slug)
    category_ids = company.active_menu.entry_list.values_list('category', flat=True).distinct()
    categories = FoodCategory.objects.filter(id__in=category_ids)
    context = {
        'company': company,
        'categories': categories,
    }
    return render(request, template_name='muglaSepeti/companies.html', context=context)
