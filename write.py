"""
write.py - Handles all file writing operations for the product system
"""

from datetime import datetime

class ProductWriter:
    """
    Handles writing product data to files including:
    - Saving product inventory
    - Generating sales invoices
    - Generating purchase invoices
    """
    
    def __init__(self, products_file="product.txt"):
        """
        Initialize the writer with the product file name
        """
        self.products_file = products_file
    
    def save_products(self, products):
        """
        Save the current product inventory to the text file.
        
        Args:
            products (dict): Dictionary of products to save
            
        Returns:
            str: Status message
        """
        try:
            with open(self.products_file, "w") as file:
                for product_id, product in products.items():
                    file.write(product['name'] + "," + product['brand'] + "," + 
                               str(product['quantity']) + "," + str(product['cost_price']) + 
                               "," + product['origin'] + "\n")
            return "\nInventory updated successfully!\n"
        except Exception as e:
            return "\nError saving products: " + str(e) + "\n"
    
    def generate_sale_invoice(self, customer_name, customer_phone, items, subtotal, shipping, total):
        """
        Generate a sales invoice text file.
        
        Args:
            customer_name (str): Name of the customer
            customer_phone (str): Phone number of the customer
            items (list): List of items purchased
            subtotal (float): Subtotal amount
            shipping (float): Shipping cost
            total (float): Grand total amount
            
        Returns:
            str: Name of the generated file or error message
        """
        now = datetime.now()
        timestamp = (
            str(now.year).zfill(4) +
            str(now.month).zfill(2) +
            str(now.day).zfill(2) + "_" +
            str(now.hour).zfill(2) +
            str(now.minute).zfill(2) +
            str(now.second).zfill(2)
        )
        formatted_time = (
            str(now.year).zfill(4) + "-" +
            str(now.month).zfill(2) + "-" +
            str(now.day).zfill(2) + " " +
            str(now.hour).zfill(2) + ":" +
            str(now.minute).zfill(2) + ":" +
            str(now.second).zfill(2)
        )
        
        filename = "Sale_" + customer_name + "_" + timestamp + ".txt"
        
        try:
            with open(filename, "w") as file:
                file.write("="*50 + "\n")
                file.write("\tWeCare Wholesale\n")
                file.write("\tKamalpokhari, Kathmandu\n")
                file.write("\tPhone: 9811112255\n")
                file.write("="*50 + "\n")
                file.write("Customer: " + customer_name + "\n")
                file.write("Phone: " + str(customer_phone) + "\n")
                file.write("Date: " + formatted_time + "\n")
                file.write("="*50 + "\n")
                file.write("Item\t\tQty\tPrice\tTotal\n")
                file.write("="*50 + "\n")
                
                for item in items:
                    file.write(item['name'] + "\t" + str(item['quantity']) + "\t" + 
                               str(item['price']) + "\t" + str(item['total']) + "\n")
                    if item.get('free_items', 0) > 0:
                        file.write("(+" + str(item['free_items']) + " free items)\n")
                
                file.write("="*50 + "\n")
                file.write("Subtotal:\t\t\t" + str(subtotal) + "\n")
                file.write("Shipping:\t\t\t" + str(shipping) + "\n")
                file.write("Grand Total:\t\t\t" + str(total) + "\n")
                file.write("="*50 + "\n")
                file.write("\tThank you for shopping with us!\n")
                file.write("="*50 + "\n")
            
            return "\nSale invoice generated: " + filename + "\n"
        except Exception as e:
            return "\nError generating invoice: " + str(e) + "\n"
    
    def generate_purchase_invoice(self, supplier_name, items, total):
        """
        Generate a purchase invoice text file.
        
        Args:
            supplier_name (str): Name of the supplier
            items (list): List of items purchased
            total (float): Total amount
            
        Returns:
            str: Name of the generated file or error message
        """
        now = datetime.now()
        timestamp = (
            str(now.year).zfill(4) +
            str(now.month).zfill(2) +
            str(now.day).zfill(2) + "_" +
            str(now.hour).zfill(2) +
            str(now.minute).zfill(2) +
            str(now.second).zfill(2)
        )
        formatted_time = (
            str(now.year).zfill(4) + "-" +
            str(now.month).zfill(2) + "-" +
            str(now.day).zfill(2) + " " +
            str(now.hour).zfill(2) + ":" +
            str(now.minute).zfill(2) + ":" +
            str(now.second).zfill(2)
        )
        
        filename = "Purchase_" + supplier_name + "_" + timestamp + ".txt"
        
        try:
            with open(filename, "w") as file:
                file.write("="*50 + "\n")
                file.write("\tWeCare Wholesale\n")
                file.write("\tKamalpokhari, Kathmandu\n")
                file.write("\tPhone: 9811112255\n")
                file.write("="*50 + "\n")
                file.write("Supplier: " + supplier_name + "\n")
                file.write("Date: " + formatted_time + "\n")
                file.write("="*50 + "\n")
                file.write("Item\t\tQty\tPrice\tTotal\n")
                file.write("="*50 + "\n")
                
                for item in items:
                    file.write(item['name'] + "\t" + str(item['quantity']) + "\t" + 
                               str(item['price']) + "\t" + str(item['total']) + "\n")
                    if item.get('is_new', False):
                        file.write("(New product added to inventory)\n")
                
                file.write("="*50 + "\n")
                file.write("Total Amount:\t\t\t" + str(total) + "\n")
                file.write("="*50 + "\n")
                file.write("\tInventory updated successfully!\n")
                file.write("="*50 + "\n")
            
            return "\nPurchase invoice generated: " + filename + "\n"
        except Exception as e:
            return "\nError generating invoice: " + str(e) + "\n"
