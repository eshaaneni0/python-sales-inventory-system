"""
main.py - The entry point for the WeCare Wholesale System
This module initializes and runs the main program loop.
"""

from operations import ProductSystem

def main():
    """
    Main function that starts the program execution.
    """
    print("\n" + "="*50)
    print("\tWelcome to WeCare Wholesale System")
    print("="*50)
    
    # Create and run the product system
    system = ProductSystem()
    system.run()

if __name__ == "__main__":
    main()
