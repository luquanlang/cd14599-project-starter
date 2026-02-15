# Udatracker Starter Code

## Project Reflection

**Design Decision**: The `OrderTracker` class uses dependency injection with a storage abstraction, validating that the injected storage implements required methods (`save_order`, `get_order`, `get_all_orders`). This trade-off prioritizes testability and flexibility over simplicity—we can easily swap storage implementations and use mocks in tests, though it adds initial complexity.

**Testing Insight**: Writing the test for invalid status validation (`test_update_order_status_with_invalid_status`) revealed the importance of fail-fast behavior. The test verifies that validation occurs *before* checking storage, preventing unnecessary database calls and improving performance. This drove a refactor to validate status early in the `update_order_status` method.

**Next Steps**: If continuing this project, I would add:
- A DELETE endpoint to remove orders
- Persistent storage (SQLite or PostgreSQL) to replace in-memory storage
- Enhanced validation (e.g., customer_id format, quantity limits)

---

This directory contains the starter code for the Udatracker project. The initial structure of directories and files is described below.

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```
