# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        # Check if the order already exists
        if self.storage.get_order(order_id):
            raise ValueError(f"Order with ID '{order_id}' already exists.")
        
        # Check if the quantity is valid
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        
        # Check order_id is not empty
        if not order_id:
            raise ValueError("order_id cannot be empty")
        
        # Check item_name is not empty
        if not item_name:
            raise ValueError("item_name cannot be empty")
        
        # Check customer_id is not empty
        if not customer_id:
            raise ValueError("customer_id cannot be empty")
    
        # Check if the status is valid
        if status and status not in ["pending", "processing", "shipped", "delivered"]:
            raise ValueError("Invalid status")
        
        # Save the order
        self.storage.save_order(order_id, {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity, 
            "customer_id": customer_id,
            "status": status or "pending"
        })

    def get_order_by_id(self, order_id: str):
        # Check if the order_id is not empty
        if not order_id:
            raise ValueError("order_id cannot be empty")
        
        # Get the order
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):

        # Check if the order_id is not empty
        if not order_id:
            raise ValueError("order_id cannot be empty")
        
          # Check if the new_status is valid
        if new_status and new_status not in ["pending", "processing", "shipped", "delivered"]:
            raise ValueError("Invalid status")

        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID '{order_id}' not found")

        order["status"] = new_status

        self.storage.save_order(order_id, order)

    def list_all_orders(self):
        return self.storage.get_all_orders()

    def list_orders_by_status(self, status: str):
        # Check if the status is not empty
        if not status:
            raise ValueError("status cannot be empty")
        
        # Check if the status is valid
        if status not in ["pending", "processing", "shipped", "delivered"]:
            raise ValueError("Invalid status")
        
        # Get the orders by status
        orders = self.storage.get_all_orders()
        return [order for order in orders.values() if order["status"] == status]
