from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List
from store.models import Product


class ShippableItem(ABC):
    #Interface for items that can be shipped
    
    @abstractmethod
    def getName(self) -> str:
        #Return the name of the item
        pass
    
    @abstractmethod
    def getWeight(self) -> float:
        #Return the weight of the item in kg
        pass


class ProductShippableItem(ShippableItem):
    #Implementation of ShippableItem for Product model
    
    def __init__(self, product: Product, quantity: int = 1):
        self.product = product
        self.quantity = quantity
    
    def getName(self) -> str:
        return str(self.product.name)
    
    def getWeight(self) -> float:
        # Convert Decimal to float and multiply by quantity
        try:
            weight = float(self.product.weight) if self.product.weight else 0.0
        except (TypeError, ValueError):
            weight = 0.0
        return weight * self.quantity


class ShippingService:
    #Service to handle shipping calculations and logistics
    
    def __init__(self):
        self.base_shipping_rate = 10.00  # Base shipping cost
        self.weight_rate = 2.00  # Additional cost per kg
    
    def calculateShippingCost(self, items: List[ShippableItem]) -> float:
        """
        Calculate shipping cost based on total weight of items
        
        Args:
            items: List of shippable items
            
        Returns:
            float: Total shipping cost
        """
        if not items:
            return 0.0
        
        total_weight = sum(item.getWeight() for item in items)
        
        # Base shipping cost + weight-based additional cost
        shipping_cost = self.base_shipping_rate + (total_weight * self.weight_rate)
        
        return round(shipping_cost, 2)
    
    def getShippingDetails(self, items: List[ShippableItem]) -> dict:
        """
        Get detailed shipping information
        
        Args:
            items: List of shippable items
            
        Returns:
            dict: Shipping details including items, weights, and costs
        """
        if not items:
            return {
                'items': [],
                'total_weight': 0.0,
                'shipping_cost': 0.0,
                'item_count': 0
            }
        
        item_details = []
        total_weight = 0.0
        
        for item in items:
            weight = item.getWeight()
            total_weight += weight
            item_details.append({
                'name': item.getName(),
                'weight': weight
            })
        
        shipping_cost = self.calculateShippingCost(items)
        
        return {
            'items': item_details,
            'total_weight': round(total_weight, 2),
            'shipping_cost': shipping_cost,
            'item_count': len(items)
        }
    
    def processShippingOrder(self, items: List[ShippableItem], customer_info: dict) -> dict:
        """
        Process a shipping order with customer information
        
        Args:
            items: List of shippable items
            customer_info: Dictionary containing customer shipping details
            
        Returns:
            dict: Shipping order details
        """
        shipping_details = self.getShippingDetails(items)
        
        # Create shipping order
        shipping_order = {
            'customer_name': customer_info.get('full_name', ''),
            'customer_email': customer_info.get('email', ''),
            'shipping_address': customer_info.get('shipping_address', ''),
            'items': shipping_details['items'],
            'total_weight': shipping_details['total_weight'],
            'shipping_cost': shipping_details['shipping_cost'],
            'item_count': shipping_details['item_count'],
            'tracking_number': self._generateTrackingNumber(),
            'status': 'pending'
        }
        
        return shipping_order
    
    def _generateTrackingNumber(self) -> str:
        #Generate a unique tracking number
        import uuid
        import time
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        return f"TRK{timestamp}{unique_id}".upper()
    



def collectShippableItems(cart_products, quantities) -> List[ShippableItem]:
    """
    Collect all items that need to be shipped from cart
    
    Args:
        cart_products: List of Product objects
        quantities: Dictionary of product_id -> quantity
        
    Returns:
        List[ShippableItem]: List of shippable items
    """
    shippable_items = []
    
    for product in cart_products:
        # Check if product is shippable
        if product.is_shippable:
            quantity = quantities.get(str(product.id), 1)
            shippable_item = ProductShippableItem(product, quantity)
            shippable_items.append(shippable_item)
    
    return shippable_items 