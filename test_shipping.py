#!/usr/bin/env python
"""
Test script for shipping service functionality
Run this script to test the shipping service with sample data
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Product
from payment.shipping_service import ShippingService, ProductShippableItem, collectShippableItems

def test_shipping_service():
    """Test the shipping service with sample data"""
    
    print("="*60)
    print("SHIPPING SERVICE TEST")
    print("="*60)
    
    # Create shipping service instance
    shipping_service = ShippingService()
    
    # Test 1: Create sample shippable items
    print("\n1. Testing ShippableItem Interface:")
    print("-" * 40)
    
    # Create sample products (these won't be saved to database)
    sample_products = [
        {'name': 'Laptop', 'weight': 2.5, 'is_shippable': True},
        {'name': 'Mouse', 'weight': 0.1, 'is_shippable': True},
        {'name': 'Digital Download', 'weight': 0.0, 'is_shippable': False},
        {'name': 'Monitor', 'weight': 5.0, 'is_shippable': True},
    ]
    
    shippable_items = []
    for product_data in sample_products:
        # Create a mock product object
        class MockProduct:
            def __init__(self, name, weight, is_shippable):
                self.name = name
                self.weight = weight
                self.is_shippable = is_shippable
        
        mock_product = MockProduct(
            product_data['name'], 
            product_data['weight'], 
            product_data['is_shippable']
        )
        
        if mock_product.is_shippable:
            item = ProductShippableItem(mock_product, quantity=2)
            shippable_items.append(item)
            print(f"✓ Created shippable item: {item.getName()} (weight: {item.getWeight()} kg)")
    
    # Test 2: Calculate shipping cost
    print(f"\n2. Shipping Cost Calculation:")
    print("-" * 40)
    shipping_cost = shipping_service.calculateShippingCost(shippable_items)
    print(f"Total shipping cost: ${shipping_cost:.2f}")
    
    # Test 3: Get shipping details
    print(f"\n3. Shipping Details:")
    print("-" * 40)
    shipping_details = shipping_service.getShippingDetails(shippable_items)
    print(f"Number of items: {shipping_details['item_count']}")
    print(f"Total weight: {shipping_details['total_weight']} kg")
    print(f"Shipping cost: ${shipping_details['shipping_cost']:.2f}")
    
    print("\nItem breakdown:")
    for item in shipping_details['items']:
        print(f"  • {item['name']}: {item['weight']} kg")
    
    # Test 4: Process shipping order
    print(f"\n4. Shipping Order Processing:")
    print("-" * 40)
    customer_info = {
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'shipping_address': '123 Main St, City, Country'
    }
    
    shipping_order = shipping_service.processShippingOrder(shippable_items, customer_info)
    print(f"Tracking Number: {shipping_order['tracking_number']}")
    print(f"Customer: {shipping_order['customer_name']}")
    print(f"Email: {shipping_order['customer_email']}")
    print(f"Total Weight: {shipping_order['total_weight']} kg")
    print(f"Shipping Cost: ${shipping_order['shipping_cost']:.2f}")
    print(f"Status: {shipping_order['status']}")
    
    print("\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*60)

def test_with_real_products():
    """Test with actual products from database"""
    
    print("\n" + "="*60)
    print("TESTING WITH REAL PRODUCTS FROM DATABASE")
    print("="*60)
    
    try:
        # Get all products from database
        products = Product.objects.all()
        
        if not products.exists():
            print("No products found in database. Please add some products first.")
            return
        
        print(f"Found {products.count()} products in database")
        
        # Create sample quantities (product_id -> quantity)
        quantities = {}
        for product in products[:3]:  # Test with first 3 products
            quantities[str(product.id)] = 2
        
        # Test collectShippableItems function
        shippable_items = collectShippableItems(products[:3], quantities)
        
        print(f"\nShippable items found: {len(shippable_items)}")
        for item in shippable_items:
            print(f"  • {item.getName()}: {item.getWeight()} kg")
        
        if shippable_items:
            shipping_service = ShippingService()
            shipping_details = shipping_service.getShippingDetails(shippable_items)
            
            print(f"\nShipping Details:")
            print(f"  Total Weight: {shipping_details['total_weight']} kg")
            print(f"  Shipping Cost: ${shipping_details['shipping_cost']:.2f}")
        
    except Exception as e:
        print(f"Error testing with real products: {e}")

if __name__ == "__main__":
    print("Starting Shipping Service Tests...")
    
    # Test with mock data
    test_shipping_service()
    
    # Test with real database data
    test_with_real_products()
    
    print("\nAll tests completed!") 