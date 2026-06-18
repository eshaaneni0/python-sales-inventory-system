"""
read.py - Handles all file reading operations for the product system
"""

class ProductReader:
    """
    Handles reading product data from the file
    """
    
    def __init__(self, filename="product.txt"):
        """
        Initialize the reader with the product file name
        """
        self.products_file = filename
    
    def load_products(self):
        """
        Load products from the text file into a dictionary.
        Returns:
            dict: A dictionary of products with IDs as keys
            str: A status message
        """
        products = {}
        try:
            with open(self.products_file, "r") as file:
                product_id = 1
                for line in file:
                    # Skip empty lines
                    if not line or line == "\n":
                        continue
                    
                    # Remove newline character the old way
                    if line.endswith('\n'):
                        line = line[:-1]
                    
                    # Split line into components
                    parts = line.split(",")
                    
                    # Ensure we have all 5 parts (name, brand, quantity, price, origin)
                    if len(parts) == 5:
                        products[product_id] = {
                            "name": parts[0],
                            "brand": parts[1],
                            "quantity": int(parts[2]),
                            "cost_price": int(parts[3]),
                            "origin": parts[4]
                        }
                        product_id += 1
                    else:
                        return {}, "Warning: Skipping invalid product entry: " + line
            
            return products, "\nProducts loaded successfully!\n"
        
        except FileNotFoundError:
            return {}, "\nError: products.txt file not found. Starting with empty inventory.\n"
        except Exception as e:
            return {}, "\nError loading products: " + str(e) + "\n"
