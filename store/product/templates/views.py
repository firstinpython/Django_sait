from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from command.views import TitleMixin

from .models import Basket, Product, ProductsCategory


# Create your views here.


class MainView(TitleMixin, TemplateView):
    template_name = 'product/index.html'
    title = 'Store'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


# def main(request):
#     context = {
#         'title': 'Store'
#     }
#     return render(request, 'product/index.html')


class ProductsListView(ListView):
    model = Product
    template_name = 'product/products.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['categories'] = ProductsCategory.objects.all()
        return context


# def products(request, category_id=None):
#     if category_id:
#         category = ProductsCategory.objects.get(id=category_id)
#         product = Product.objects.filter(category=category)
#         category_page = True
#     else:
#         product = Product.objects.all()
#         category_page = False
#     PER_PAGE = 3
#     paginator = Paginator(product, PER_PAGE)
#     page = request.GET.get('page')
#     products_paginatore = paginator.get_page(page)
#     context = {
#         'title': 'Store - Каталог',
#         'products': products_paginatore,
#         'categories': ProductsCategory.objects.all(),
#         'category_page': category_page
#     }
#     return render(request, 'product/products.html', context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if product.quantity != 0:
        if not baskets.exists():

            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket_changes = baskets.first()
            basket_changes.quantity += 1
            basket_changes.save()
            # product_changes = product
            # product_changes.quantity -=1
            # Product.save(product_changes)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
