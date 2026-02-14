import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)


# ==========================================
# Tests for add_order
# ==========================================

def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    # Act
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    # Assert
    mock_storage.save_order.assert_called_once()


def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Arrange
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    # Act & Assert
    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")


def test_add_order_with_explicit_status(order_tracker, mock_storage):
    """Tests adding a new order with an explicitly set valid status."""
    # Act
    order_tracker.add_order("ORD002", "Mouse", 2, "CUST002", status="processing")

    # Assert
    mock_storage.save_order.assert_called_once()
    saved_order = mock_storage.save_order.call_args[0][1]
    assert saved_order['status'] == "processing"


def test_add_order_with_invalid_quantity_zero(order_tracker, mock_storage):
    """Tests that adding an order with quantity=0 raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        order_tracker.add_order("ORD003", "Keyboard", 0, "CUST003")


def test_add_order_with_invalid_quantity_negative(order_tracker, mock_storage):
    """Tests that adding an order with negative quantity raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        order_tracker.add_order("ORD004", "Monitor", -5, "CUST004")


def test_add_order_with_empty_order_id(order_tracker, mock_storage):
    """Tests that adding an order with empty order_id raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="order_id cannot be empty"):
        order_tracker.add_order("", "Tablet", 1, "CUST005")


def test_add_order_with_none_order_id(order_tracker, mock_storage):
    """Tests that adding an order with None order_id raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="order_id cannot be empty"):
        order_tracker.add_order(None, "Tablet", 1, "CUST005")


def test_add_order_with_empty_item_name(order_tracker, mock_storage):
    """Tests that adding an order with empty item_name raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="item_name cannot be empty"):
        order_tracker.add_order("ORD006", "", 1, "CUST006")


def test_add_order_with_empty_customer_id(order_tracker, mock_storage):
    """Tests that adding an order with empty customer_id raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="customer_id cannot be empty"):
        order_tracker.add_order("ORD007", "Headphones", 1, "")


def test_add_order_with_invalid_initial_status(order_tracker, mock_storage):
    """Tests that adding an order with an invalid status raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid status"):
        order_tracker.add_order("ORD008", "Speaker", 1, "CUST008", status="invalid_status")


# ==========================================
# Tests for get_order_by_id
# ==========================================

def test_get_order_by_id_existing_order(order_tracker, mock_storage):
    """Tests retrieving an existing order by its ID."""
    # Arrange
    expected_order = {
        "order_id": "ORD100",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST100",
        "status": "pending"
    }
    mock_storage.get_order.return_value = expected_order

    # Act
    result = order_tracker.get_order_by_id("ORD100")

    # Assert
    assert result == expected_order
    mock_storage.get_order.assert_called_once_with("ORD100")


def test_get_order_by_id_non_existent_order(order_tracker, mock_storage):
    """Tests that retrieving a non-existent order returns None."""
    # Arrange
    mock_storage.get_order.return_value = None

    # Act
    result = order_tracker.get_order_by_id("ORD999")

    # Assert
    assert result is None
    mock_storage.get_order.assert_called_once_with("ORD999")


def test_get_order_by_id_with_empty_id(order_tracker, mock_storage):
    """Tests that retrieving an order with empty ID raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="order_id cannot be empty"):
        order_tracker.get_order_by_id("")


def test_get_order_by_id_with_none_id(order_tracker, mock_storage):
    """Tests that retrieving an order with None ID raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="order_id cannot be empty"):
        order_tracker.get_order_by_id(None)


# ==========================================
# Tests for update_order_status
# ==========================================

def test_update_order_status_successfully(order_tracker, mock_storage):
    """Tests successfully updating an order's status."""
    # Arrange
    existing_order = {
        "order_id": "ORD200",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST200",
        "status": "pending"
    }
    mock_storage.get_order.return_value = existing_order

    # Act
    order_tracker.update_order_status("ORD200", "shipped")

    # Assert
    mock_storage.get_order.assert_called_once_with("ORD200")
    mock_storage.save_order.assert_called_once()
    updated_order = mock_storage.save_order.call_args[0][1]
    assert updated_order["status"] == "shipped"

def test_update_order_status_with_invalid_status(order_tracker, mock_storage):
    """Tests that updating to an invalid status raises ValueError before checking storage."""
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid status"):
        order_tracker.update_order_status("ORD201", "invalid_status")

    # Assert (verify fail-fast behavior - no storage read)
    mock_storage.get_order.assert_not_called()


def test_update_order_status_for_non_existent_order(order_tracker, mock_storage):
    """Tests that updating a non-existent order raises a ValueError."""
    # Arrange
    mock_storage.get_order.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="Order with ID 'ORD999' not found"):
        order_tracker.update_order_status("ORD999", "shipped")


def test_update_order_status_with_empty_id(order_tracker, mock_storage):
    """Tests that updating an order with empty ID raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="order_id cannot be empty"):
        order_tracker.update_order_status("", "shipped")


# ==========================================
# Tests for list_all_orders
# ==========================================

def test_list_all_orders_empty_storage(order_tracker, mock_storage):
    """Tests listing all orders when storage is empty."""
    # Arrange
    mock_storage.get_all_orders.return_value = []

    # Act
    result = order_tracker.list_all_orders()

    # Assert
    assert result == []
    mock_storage.get_all_orders.assert_called_once()


def test_list_all_orders_multiple_orders(order_tracker, mock_storage):
    """Tests listing all orders when storage has multiple orders."""
    # Arrange
    orders_dict = {
        "ORD300": {
            "order_id": "ORD300",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST300",
            "status": "pending"
        },
        "ORD301": {
            "order_id": "ORD301",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST301",
            "status": "shipped"
        },
        "ORD302": {
            "order_id": "ORD302",
            "item_name": "Keyboard",
            "quantity": 1,
            "customer_id": "CUST302",
            "status": "delivered"
        }
    }
    mock_storage.get_all_orders.return_value = orders_dict

    # Act
    result = order_tracker.list_all_orders()

    # Assert
    assert len(result) == 3
    assert all(order in result.values() for order in orders_dict.values())


# ==========================================
# Tests for list_orders_by_status
# ==========================================

def test_list_orders_by_status_with_matches(order_tracker, mock_storage):
    """Tests listing orders filtered by status when there are matches."""
    # Arrange
    orders_dict = {
        "ORD400": {
            "order_id": "ORD400",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST400",
            "status": "shipped"
        },
        "ORD401": {
            "order_id": "ORD401",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST401",
            "status": "pending"
        },
        "ORD402": {
            "order_id": "ORD402",
            "item_name": "Keyboard",
            "quantity": 1,
            "customer_id": "CUST402",
            "status": "shipped"
        }
    }
    mock_storage.get_all_orders.return_value = orders_dict

    # Act
    result = order_tracker.list_orders_by_status("shipped")

    # Assert
    assert len(result) == 2
    assert all(order["status"] == "shipped" for order in result)
    assert orders_dict["ORD400"] in result
    assert orders_dict["ORD402"] in result


def test_list_orders_by_status_with_no_matches(order_tracker, mock_storage):
    """Tests listing orders filtered by status when there are no matches."""
    # Arrange
    orders_dict = {
        "ORD500": {
            "order_id": "ORD500",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST500",
            "status": "pending"
        }
    }
    mock_storage.get_all_orders.return_value = orders_dict

    # Act
    result = order_tracker.list_orders_by_status("shipped")

    # Assert
    assert result == []


def test_list_orders_by_status_empty_storage(order_tracker, mock_storage):
    """Tests listing orders by status when storage is empty."""
    # Arrange
    mock_storage.get_all_orders.return_value = {}

    # Act
    result = order_tracker.list_orders_by_status("pending")

    # Assert
    assert result == []


def test_list_orders_by_status_with_empty_status(order_tracker, mock_storage):
    """Tests that listing orders with empty status raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="status cannot be empty"):
        order_tracker.list_orders_by_status("")


def test_list_orders_by_status_with_invalid_status(order_tracker, mock_storage):
    """Tests that listing orders with invalid status raises a ValueError."""
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid status"):
        order_tracker.list_orders_by_status("invalid_status")
