from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.http import HttpResponse
from datetime import datetime


class SalesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            sales = Sale.objects.filter(product__branch=request.user.branch).order_by('-sold_at')
            products = Product.objects.filter(branch=request.user.branch)
            clients = Client.objects.filter(branch=request.user.branch)
            context = {
                'sales': sales,
                'products': products,
                'clients': clients,
            }
            return render(request, 'sales.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=request.POST.get('product_id'))
            client = get_object_or_404(Client, id=request.POST.get('client_id'))

            amount = float(request.POST.get('amount'))
            if amount > product.amount:
                return HttpResponse(
                    f"""
                    <h2>{product.name} miqdori yetarlicha mavjud emas! Mavjud: {product.amount} {product.unit}</h2>
                    <a href="/stats/sales/">Ortga</a>
                    """
                )
            total_price = None if request.POST.get('total_price') == "" else float(request.POST.get('total_price'))
            paid_price = None if request.POST.get('paid_price') == "" else float(request.POST.get('paid_price'))
            debt_price = None if request.POST.get('debt_price') == "" else float(request.POST.get('debt_price'))

            if total_price is None:
                total_price = product.export_price * amount

            if debt_price is None or paid_price is None:
                if paid_price is not None:
                    debt_price = total_price - paid_price
                elif debt_price is not None:
                    paid_price = total_price - debt_price
                else:
                    paid_price = total_price
                    debt_price = 0

            sold_at = datetime.now() if request.POST.get('sold_at') == "" else request.POST.get('sold_at')

            Sale.objects.create(
                product=product,
                client=client,
                amount=amount,
                sold_at=sold_at,
                total_price=total_price,
                paid_price=paid_price,
                debt_price=debt_price,
                branch=request.user.branch,
            )

            product.amount -= amount
            product.save()

            client.debt += debt_price
            client.save()

            return redirect('sales')
        return redirect('login')


class SaleUpdateView(View):
    def get(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk)
        products = Product.objects.all()
        clients = Client.objects.all()
        context = {
            'sale': sale,
            'products': products,
            'clients': clients,
        }
        return render(request, 'sale-edit.html', context)

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=request.POST.get('client_id'))
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        Sale.objects.filter(pk=pk).update(
            client=client,
            product=product,
            amount=request.POST.get('amount'),
            sold_at=request.POST.get('sold_at'),
            total_price=request.POST.get('total_price'),
            paid_price=request.POST.get('paid_price'),
            debt_price=request.POST.get('debt_price'),

        )
        return redirect('sales')


class SaleDeleteView(View):
    def get(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk)
        context = {
            'sale': sale,
        }
        return render(request, 'sale-delete.html', context)

    def post(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk)
        sale.delete()
        return redirect('sales')


class ImportsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            imports = Import.objects.all()
            products = Product.objects.filter(branch=request.user.branch)
            context = {
                'imports': imports,
                'products': products
            }
            return render(request, 'imports.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=request.POST.get('product_id'))
            amount = float(request.POST.get('amount'))

            total_price = None if request.POST.get('total_price') == "" else float(request.POST.get('total_price'))
            per_price = None if request.POST.get('per_price') == "" else request.POST.get('per_price')
            if total_price is None:
                total_price = per_price * amount

            Import.objects.create(
                deliverer=request.POST.get('deliverer'),
                product=product,
                amount=amount,
                per_price=per_price,
                total_price=total_price,
                created_at=request.POST.get('created_at'),
                branch=request.user.branch,
            )
            product.amount += amount
            product.save()
            return redirect('imports')
        return redirect('login')


class ImportUpdateView(View):
    def get(self, request, pk):
        imported = get_object_or_404(Import, pk=pk)
        products = Product.objects.filter(branch=request.user.branch)
        context = {
            'imported': imported,
            'products': products,
        }
        return render(request, 'import-edit.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=request.POST.get('product_id'))
        Import.objects.filter(id=pk).update(
            deliverer=request.POST.get('deliverer'),
            product=product,
            amount=request.POST.get('amount'),
            per_price=request.POST.get('per_price'),
            total_price=request.POST.get('total_price'),
            created_at=request.POST.get('created_at'),
            branch=request.user.branch,
        )
        return redirect('imports')


class ImportDeleteView(View):
    def get(self, request, pk):
        imported = get_object_or_404(Import, pk=pk)
        context = {
            'imported': imported
        }
        return render(request, 'import-delete.html', context)

    def post(self, request, pk):
        imported = get_object_or_404(Import, pk=pk)
        imported.delete()
        return redirect('imports')



