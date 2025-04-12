import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Blog, Bill, Stock, Item
from .forms import BillForm, BillItemForm
from django.contrib import messages
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook

# Home View
def home(request):
    messages.success(request, "Welcome to the Django App!")
    return HttpResponse("Welcome to Djangoapp!")

# Example View
def example_view(request):
    try:
        post = Blog.objects.all()
        messages.success(request, "Posts loaded successfully!")
        return render(request, 'base.html', {'post': post})
    except Exception as e:
        messages.error(request, f"Error loading posts: {e}")
        return render(request, 'base.html', {'post': []})

# Navbar View
def navbar_view(request):
    try:
        return render(request, 'navbar.html')
    except Exception as e:
        messages.error(request, f"Error loading navbar: {e}")
        return render(request, 'navbar.html')

# Dashboard View
def dashboard_view(request):
    try:
        Bill_datails = Bill.objects.all()
        if 'export' in request.GET:
            # Create an Excel workbook
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Bill Details"

            # Add headers
            headers = ['Customer Name', 'Customer Phone', 'Purchase Date', 'Subtotal', 'GST', 'Total', 'Item Names']
            sheet.append(headers)

            # Add data rows
            for bill in Bill_datails:
                item_names = ', '.join([item['item_name'] for item in bill.items])
                sheet.append([
                    bill.customer_name,
                    bill.customer_phone,
                    bill.purchase_date.strftime('%Y-%m-%d %H:%M:%S'),
                    bill.Sub_total,
                    bill.GST,
                    bill.Total,
                    item_names
                ])

            # Set the response
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="bill_details.xlsx"'
            workbook.save(response)
            messages.success(request, "Bill details exported successfully!")
            return response

        return render(request, 'dashboard.html', {'Bill_datails': Bill_datails})
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {e}")
        return render(request, 'dashboard.html', {'Bill_datails': []})

# Stock View
def stock_view(request):
    try:
        stock_data = Stock.objects.all()

        # Prepare data for the pie chart
        labels = [stock.category_name for stock in stock_data]
        initial_stock_values = [stock.initial_stock for stock in stock_data]
        current_stock_values = [stock.current_stock for stock in stock_data]
        total_sold_values = [stock.initial_stock - stock.current_stock for stock in stock_data]

        messages.success(request, "Stock data loaded successfully!")
        return render(request, 'stockdetails.html', {
            'stock_data': stock_data,
            'labels': json.dumps(labels),
            'initial_stock_values': json.dumps(initial_stock_values),
            'current_stock_values': json.dumps(current_stock_values),
            'total_sold_values': json.dumps(total_sold_values),
        })
    except Exception as e:
        messages.error(request, f"Error loading stock data: {e}")
        return render(request, 'stockdetails.html', {})

# Bill Data View
def bill_data(request):
    BillItemFormSet = formset_factory(BillItemForm, extra=1)
    preview_data = None
    saved_bill = None

    try:
        if request.method == 'POST':
            bill_form = BillForm(request.POST)
            item_formset = BillItemFormSet(request.POST)

            if 'preview' in request.POST:
                if bill_form.is_valid() and item_formset.is_valid():
                    preview_data = {
                        'customer_name': bill_form.cleaned_data['customer_name'],
                        'customer_phone': bill_form.cleaned_data['customer_phone'],
                        'items': []
                    }
                    subtotal = 0
                    for form in item_formset:
                        # Process only valid forms with data
                        if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                            category = form.cleaned_data['category']
                            item = form.cleaned_data['item']
                            quantity = form.cleaned_data['quantity']
                            rate = form.cleaned_data['rate']
                            item_total = quantity * rate
                            subtotal += item_total
                            preview_data['items'].append({
                                'category': category.category_name,
                                'item_name': item.item_name,
                                'quantity': quantity,
                                'rate': rate,
                                'total': item_total
                            })
                    gst = subtotal * 0.03
                    total = subtotal + gst
                    preview_data['subtotal'] = subtotal
                    preview_data['gst'] = gst
                    preview_data['total'] = total
                    messages.info(request, "Preview the data before submitting.")
                else:
                    messages.error(request, "Form validation failed for preview.")

            elif 'submit' in request.POST:
                if bill_form.is_valid() and item_formset.is_valid():
                    bill = bill_form.save(commit=False)
                    items = []
                    subtotal = 0
                    for form in item_formset:
                        # Process only valid forms with data
                        if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                            category = form.cleaned_data['category']
                            item = form.cleaned_data['item']
                            quantity = form.cleaned_data['quantity']
                            rate = form.cleaned_data['rate']
                            item_total = quantity * rate
                            subtotal += item_total
                            items.append({
                                'category': category.category_name,
                                'item_name': item.item_name,
                                'item_id': item.id,
                                'quantity': quantity,
                                'rate': rate,
                                'total': item_total
                            })
                    gst = subtotal * 0.03
                    total = subtotal + gst
                    bill.Sub_total = subtotal
                    bill.GST = gst
                    bill.Total = total
                    bill.items = items
                    bill.save()
                    saved_bill = bill
                    messages.success(request, "Bill saved successfully!")
                else:
                    messages.error(request, "Form validation failed for submission.")
        else:
            bill_form = BillForm()
            item_formset = BillItemFormSet()
    except Exception as e:
        messages.error(request, f"Error processing bill data: {e}")

    return render(request, 'bill_data.html', {
        'form': bill_form,
        'item_formset': item_formset,
        'preview_data': preview_data,
        'saved_bill': saved_bill
    })
# Get Items View
def get_items(request, category_id):
    try:
        items = Item.objects.filter(stock_id=category_id).values('id', 'item_name')
        return JsonResponse({'items': list(items)})
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Add Item View
@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_id = data.get('category')
            item_name = data.get('item_name')

            category = Stock.objects.get(id=category_id)
            new_item = Item.objects.create(stock=category, item_name=item_name)

            messages.success(request, "Item added successfully!")
            return JsonResponse({
                'success': True,
                'item': {
                    'id': new_item.id,
                    'item_name': new_item.item_name
                }
            })
        except Exception as e:
            messages.error(request, f"Error adding item: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Print Bill View
def print_bill(request, bill_id):
    try:
        bill = get_object_or_404(Bill, id=bill_id)
        cgst = bill.GST / 2
        sgst = bill.GST / 2
        messages.success(request, "Bill loaded successfully!")
        return render(request, 'print_bill.html', {'bill': bill,'cgst': cgst,'sgst': sgst})
    except Exception as e:
        messages.error(request, f"Error loading bill: {e}")
        return render(request, 'print_bill.html', {'bill': None})

# Item Tables View
def item_tables_view(request):
    try:
        stocks = Stock.objects.prefetch_related('item_set')
        messages.success(request, "Stock data loaded successfully!")
        return render(request, 'items.html', {'stocks': stocks})
    except Exception as e:
        messages.error(request, f"Error loading stock data: {e}")
        return render(request, 'items.html', {'stocks': []})