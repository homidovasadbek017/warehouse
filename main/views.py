from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View


def base_view(request):
    return redirect('sections')


class SectionsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'sections.html')
        return redirect('login')


class ProductsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            products = Product.objects.order_by('-id')
            context = {
                'products': products
            }
            return render(request, 'products.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            export_price = request.POST.get('export_price')
            if export_price == '':
                export_price = None
            Product.objects.create(
                name=request.POST.get('name'),
                brand=request.POST.get('brand'),
                import_price=request.POST.get('import_price'),
                export_price=export_price,
                amount=request.POST.get('amount'),
                unit=request.POST.get('unit'),
                branch=Branch.objects.first(),
            )
            return redirect('products')
        return redirect('login')


class ProductUpdateView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=pk)
            context = {
                'product': product,
            }
            return render(request, 'product-edit.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            Product.objects.filter(pk=pk).update(
                name=request.POST.get('name'),
                brand=request.POST.get('brand'),
                import_price=request.POST.get('import_price'),
                export_price=None if request.POST.get('export_price') == "" else request.POST.get('export_price'),
                amount=request.POST.get('amount'),
                unit=request.POST.get('unit'),
            )
            return redirect('products')
        return redirect('login')


class ProductDeleteView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=pk)
            context = {
                'product': product,
            }
            return render(request, 'product-delete.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return redirect('products')
        return redirect('login')


class ClientsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            clients = Client.objects.filter(branch=request.user.branch).order_by('-debt')
            context = {
                'clients': clients,
            }
            return render(request, 'clients.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            Client.objects.create(
                name=request.POST.get('name'),
                market=request.POST.get('market'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                debt=request.POST.get('debt'),
                branch=request.user.branch,
            )
            return redirect('clients')
        return redirect('login')


class ClientUpdateView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            client = get_object_or_404(Client, pk=pk)
            context = {
                'client': client,
            }
            return render(request, 'client-edit.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            Client.objects.filter(pk=pk).update(
                name=request.POST.get('name'),
                market=request.POST.get('market'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                debt=request.POST.get('debt'),
            )
            return redirect('clients')


class ClientDeleteView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            client = get_object_or_404(Client, pk=pk)
            context = {
                'client': client,
            }
            return render(request, 'client-delete.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            client = get_object_or_404(Client, pk=pk)
            client.delete()
            return redirect('clients')
        return redirect('login')
