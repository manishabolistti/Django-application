from datetime import datetime
from django.db import models, transaction

class Blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class Stock(models.Model):
    category_name = models.CharField(max_length=100)  # Category name (e.g., Electronics, Groceries)
    initial_stock = models.FloatField(default=0.0)  # Initial stock when the category is added
    current_stock = models.FloatField(default=0.0)  # Remaining stock after sales
    total_sold = models.FloatField(default=0.0)  # Total quantity sold

    def save(self, *args, **kwargs):
        # Set current_stock equal to initial_stock for new stock entries
        if not self.pk:  # If this is a new entry
            self.current_stock = self.initial_stock
        super().save(*args, **kwargs)  # Save the updated stock details

    def __str__(self):
        return self.category_name


class Item(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)  # Link to the stock category
    item_name = models.CharField(max_length=100)  # Name of the item

    def __str__(self):
        return f"{self.item_name} ({self.stock.category_name})"


class Bill(models.Model):
    customer_name = models.CharField(max_length=100)  # Name of the customer
    customer_phone = models.CharField(max_length=15)  # Phone number of the customer
    purchase_date = models.DateTimeField(auto_now_add=True)  # Date of the purchase
    Sub_total = models.FloatField(default=0.0)  # Subtotal before GST
    GST = models.FloatField(default=0.0)  # GST amount
    Total = models.FloatField(default=0.0)  # Total amount after GST
    items = models.JSONField(default=list)  # Store multiple items as JSON

    def save(self, *args, **kwargs):
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Validate the items structure
            for item in self.items:
                if not all(key in item for key in ['category', 'item_name', 'quantity', 'rate', 'total']):
                    raise ValueError("Each item must include 'category', 'item_name', 'quantity', 'rate', and 'total'.")

                # Fetch the item and its stock
                item_obj = Item.objects.get(id=item['item_id'])
                stock_item = item_obj.stock

                # Check stock availability
                if stock_item.current_stock >= item['quantity']:
                    stock_item.current_stock -= item['quantity']  # Reduce stock
                    stock_item.total_sold += item['quantity']  # Increase total sold
                    stock_item.save()
                else:
                    raise ValueError(f"Not enough stock available for {item_obj.item_name}")

            # Calculate the subtotal dynamically based on the items
            self.Sub_total = sum(item['quantity'] * item['rate'] for item in self.items)

            # Calculate GST (e.g., 3% GST)
            gst_rate = 0.03  # 3% GST
            self.GST = self.Sub_total * gst_rate

            # Calculate the total amount
            self.Total = self.Sub_total + self.GST

            # Save the bill record
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for {self.customer_name} - Total: {self.Total}" 