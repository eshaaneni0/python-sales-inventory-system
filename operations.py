"""
operation.py - Contains all business logic and operations for the product system
"""

from datetime import datetime
from read import ProductReader
from write import ProductWriter

class ProductSystem:
    """
    A class to manage the skin care product wholesale system.
    Handles inventory management, sales, purchases, and billing.
    """
    
    def __init__(self):
        """
        Initialize the system by loading products from file.
        """
        self.reader = ProductReader()
        self.writer = ProductWriter()
        self.products = {}
        self.load_products()
    
    def layout(self, text, width, align='left'):
        """
        Custom layout function to replace ljust/rjust/center
        
        Args:
            text (str): The string to format
            width (int): Total width of the output string
            align (str): Alignment type ('left', 'right', or 'center')
            
        Returns:
            str: Formatted string with proper alignment
        """
        if len(text) >= width:
            return text[:width]  # Truncate if longer than width
        
        padding = width - len(text)
        if align == 'left':
            return text + ' ' * padding  # Add spaces to the right
        elif align == 'right':
            return ' ' * padding + text  # Add spaces to the left
        elif align == 'center':
            left = padding // 2
            right = padding - left
            return ' ' * left + text + ' ' * right  # Center with spaces
        else:
            return text  # Return as-is if invalid alignment
    
    def load_products(self):
        """
        Load products from file using the ProductReader.
        """
        self.products, message = self.reader.load_products()
        print(message)
    
    def save_products(self):
        """
        Save products to file using the ProductWriter.
        """
        message = self.writer.save_products(self.products)
        print(message)
    
    def display_products(self):
        """
        Display all available products in a properly aligned table.
        Shows both cost price (for admin) and selling price (200% markup).
        """
        # Define column widths
        col_widths = {
            'id': 5,
            'name': 20,
            'brand': 15,
            'quantity': 10,
            'cost': 12,
            'sell': 15,
            'origin': 15
        }
        
        print("\n" + "=" * 110)
        # Header row using our layout function for left alignment
        header = (
            self.layout("ID", col_widths['id']) + " " +
            self.layout("Product Name", col_widths['name']) + " " +
            self.layout("Brand", col_widths['brand']) + " " +
            self.layout("Available", col_widths['quantity']) + " " +
            self.layout("Cost Price", col_widths['cost']) + " " +
            self.layout("Selling Price", col_widths['sell']) + " " +
            self.layout("Origin", col_widths['origin'])
        )
        print(header)
        print("=" * 110)
        
        for product_id, product in self.products.items():
            selling_price = product["cost_price"] * 2  # 200% markup
            
            # Format each field with consistent lengths
            pid = self.layout(str(product_id), col_widths['id'])
            
            # Handle long names with ellipsis
            pname = product['name']
            if len(pname) > col_widths['name']:
                pname = pname[:col_widths['name']-2] + ".."
            pname = self.layout(pname, col_widths['name'])
            
            # Handle long brands with ellipsis
            pbrand = product['brand']
            if len(pbrand) > col_widths['brand']:
                pbrand = pbrand[:col_widths['brand']-2] + ".."
            pbrand = self.layout(pbrand, col_widths['brand'])
            
            pquantity = self.layout(str(product['quantity']), col_widths['quantity'])
            pcost = self.layout(str(product['cost_price']), col_widths['cost'])
            psell = self.layout(str(selling_price), col_widths['sell'])
            
            # Handle long origins with ellipsis
            porigin = product['origin']
            if len(porigin) > col_widths['origin']:
                porigin = porigin[:col_widths['origin']-2] + ".."
            porigin = self.layout(porigin, col_widths['origin'])
            
            # Build the output line
            output = (
                pid + " " +
                pname + " " +
                pbrand + " " +
                pquantity + " " +
                pcost + " " +
                psell + " " +
                porigin
            )
            print(output)
        
        print("=" * 110 + "\n")
    
    def process_sale(self):
        """
        Handle the sales process including:
        - Customer details
        - Product selection
        - Quantity with free items (buy 3 get 1 free)
        - Bill generation
        - Inventory update
        """
        print("\n" + "="*50)
        print("PRODUCT SALE PROCESS")
        print("="*50)
        
        # Get customer details
        customer_name = input("Enter customer name: ")
        
        # Get phone number with validation
        while True:
            try:
                customer_phone = int(input("Enter customer phone number: "))
                break
            except ValueError:
                print("Invalid phone number! Please enter numbers only.")
        
        sale_items = []
        total_amount = 0
        continue_shopping = True
        
        while continue_shopping:
            self.display_products()
            
            try:
                # Get product selection
                product_id = int(input("\nEnter product ID to sell (0 to finish): "))
                
                if product_id == 0:
                    continue_shopping = False
                    continue
                
                if product_id not in self.products:
                    print("Invalid product ID! Please try again.")
                    continue
                
                # Get quantity
                quantity = int(input("Enter quantity to sell: "))
                
                if quantity <= 0:
                    print("Quantity must be positive!")
                    continue
                
                product = self.products[product_id]
                
                # Calculate free items (buy 3 get 1 free)
                free_items = quantity // 3
                total_deduction = quantity + free_items
                
                # Check stock availability
                if total_deduction > product["quantity"]:
                    print("Not enough stock! Only " + str(product["quantity"]) + " available.")
                    continue
                
                # Calculate item total
                selling_price = product["cost_price"] * 2
                item_total = selling_price * quantity
                
                # Add to sale items
                sale_items.append({
                    "product_id": product_id,
                    "name": product["name"],
                    "brand": product["brand"],
                    "quantity": quantity,
                    "free_items": free_items,
                    "price": selling_price,
                    "total": item_total
                })
                
                # Update inventory
                product["quantity"] -= total_deduction
                
                # Update total
                total_amount += item_total
                
                print("\nAdded " + str(quantity) + " " + product['name'] + " (+" + str(free_items) + 
                      " free) to cart. Current total: " + str(total_amount))
            
            except ValueError:
                print("Invalid input! Please enter numbers only.")
        
        if len(sale_items) > 0:
            # Calculate shipping (free for orders over 1000)
            shipping_cost = 0 if total_amount >= 1000 else 100
            grand_total = total_amount + shipping_cost
            
            # Generate invoice
            message = self.writer.generate_sale_invoice(
                customer_name, customer_phone, sale_items, 
                total_amount, shipping_cost, grand_total
            )
            print(message)
            
            # Save updated inventory
            self.save_products()
        else:
            print("\nSale process cancelled. No products were purchased.\n")
    
    def process_purchase(self):
        """
        Handle the purchase/restocking process including:
        - Supplier details
        - Product selection (existing or new)
        - Quantity and price
        - Bill generation
        - Inventory update
        """
        print("\n" + "="*50)
        print("PRODUCT PURCHASE/RESTOCK PROCESS")
        print("="*50)
        
        # Get supplier details
        supplier_name = input("Enter supplier name: ")
        
        purchase_items = []
        total_amount = 0
        continue_purchasing = True
        
        while continue_purchasing:
            self.display_products()
            print("\n0. Finish purchase")
            print("1. Add existing product")
            print("2. Add new product")
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == 0:
                    continue_purchasing = False
                    continue
                
                

                elif choice == 1:
                    # Purchase existing product
                    product_id = int(input("Enter product ID to purchase: "))
                    
                    if product_id not in self.products:
                        print("Invalid product ID! Please try again.")
                        continue
                    
                    product = self.products[product_id]
                    
                    quantity = int(input("Enter quantity to purchase (current stock: " + str(product['quantity']) + "): "))
                    if quantity <= 0:
                        print("Quantity must be positive!")
                        continue
                    
                    # Get new cost price (optional update) with proper validation
                    while True:  # Keep asking until we get valid input
                        update_price = input("Current cost price: " + str(product['cost_price']) + ". Update price? (y/n): ").lower()
                        if update_price == 'y':
                            new_price = int(input("Enter new cost price: "))
                            if new_price <= 0:
                                print("Price must be positive! Keeping current price.")
                            else:
                                product["cost_price"] = new_price
                            break  # Exit the validation loop
                        elif update_price == 'n':
                            break  # Exit the validation loop
                        else:
                            print("Invalid input! Please enter 'y' or 'n' only.")
                    
                    # Calculate item total
                    item_total = product["cost_price"] * quantity
                    
                    # Add to purchase items
                    purchase_items.append({
                        "product_id": product_id,
                        "name": product["name"],
                        "brand": product["brand"],
                        "quantity": quantity,
                        "price": product["cost_price"],
                        "total": item_total,
                        "is_new": False
                    })
                    
                    # Update inventory
                    product["quantity"] += quantity
                    
                    # Update total
                    total_amount += item_total
                    
                    print("\nAdded " + str(quantity) + " " + product['name'] + " to purchase. Current total: " + str(total_amount))

                
                
                elif choice == 2:
                    # Add new product
                    print("\nEnter details for new product:")
                    name = input("Product name: ")
                    brand = input("Brand: ")
                    
                    quantity = int(input("Quantity: "))
                    if quantity <= 0:
                        print("Quantity must be positive!")
                        continue
                    
                    cost_price = int(input("Cost price: "))
                    if cost_price <= 0:
                        print("Price must be positive!")
                        continue
                    
                    origin = input("Country of origin: ")
                    
                    # Create new product ID
                    new_id = max(self.products.keys()) + 1 if self.products else 1
                    
                    # Add to products
                    self.products[new_id] = {
                        "name": name,
                        "brand": brand,
                        "quantity": quantity,
                        "cost_price": cost_price,
                        "origin": origin
                    }
                    
                    # Calculate item total
                    item_total = cost_price * quantity
                    
                    # Add to purchase items
                    purchase_items.append({
                        "product_id": new_id,
                        "name": name,
                        "brand": brand,
                        "quantity": quantity,
                        "price": cost_price,
                        "total": item_total,
                        "is_new": True
                    })
                    
                    # Update total
                    total_amount += item_total
                    
                    print("\nAdded new product " + name + " to inventory. Current total: " + str(total_amount))
                
                else:
                    print("Invalid choice! Please try again.")
            
            except ValueError:
                print("Invalid input! Please enter numbers only.")
        
        if len(purchase_items) > 0:
            # Generate purchase invoice
            message = self.writer.generate_purchase_invoice(supplier_name, purchase_items, total_amount)
            print(message)
            
            # Save updated inventory
            self.save_products()
        else:
            print("\nPurchase process cancelled. No products were added.\n")
    
    def run(self):
        """
        Main program loop with menu system.
        """
        while True:
            print("\n" + "="*50)
            print("\tWeCare Wholesale - Main Menu")
            print("="*50)
            print("1. Display Products")
            print("2. Process Sell")
            print("3. Process Purchase/Restock")
            print("4. Exit")
            print("="*50)
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == 1:
                    self.display_products()
                elif choice == 2:
                    self.process_sale()
                elif choice == 3:
                    self.process_purchase()
                elif choice == 4:
                    print("\nThank you for using WeCare Wholesale System. Goodbye!\n")
                    break
                else:
                    print("Invalid choice! Please enter 1-4.")
            
            except ValueError:
                print("Invalid input! Please enter a number.")
