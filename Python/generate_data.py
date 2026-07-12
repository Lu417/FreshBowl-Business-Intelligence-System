import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# -----------------------------
# Basic settings
# -----------------------------
random.seed(417)

CUSTOMER_COUNT = 100
ORDER_COUNT = 500

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR.parent / "Database" / "FreshBowl.db"


# -----------------------------
# Fixed business data
# -----------------------------
stores = [
    (1, "Adelaide CBD", "Adelaide", "SA", "2020-01-01"),
    (2, "Mawson Lakes", "Adelaide", "SA", "2021-06-01"),
    (3, "Glenelg", "Adelaide", "SA", "2022-03-01"),
]

products = [
    (1, "Chicken Bowl", "Bowl", 15.90, 7.50, 650),
    (2, "Beef Bowl", "Bowl", 16.90, 8.20, 700),
    (3, "Salmon Bowl", "Bowl", 18.90, 9.40, 620),
    (4, "Tofu Bowl", "Bowl", 14.90, 6.20, 540),
    (5, "Chicken Wrap", "Wrap", 12.90, 5.80, 520),
    (6, "Beef Wrap", "Wrap", 13.90, 6.20, 560),
    (7, "Chicken Salad", "Salad", 14.90, 6.80, 420),
    (8, "Tofu Salad", "Salad", 13.90, 5.90, 360),
    (9, "Coke", "Drink", 4.50, 1.20, 180),
    (10, "Sprite", "Drink", 4.50, 1.20, 170),
    (11, "Orange Juice", "Drink", 5.00, 1.50, 150),
    (12, "Sparkling Water", "Drink", 4.00, 0.90, 0),
    (13, "Cookie", "Snack", 3.00, 0.80, 220),
    (14, "Protein Cookie", "Snack", 4.50, 1.20, 250),
    (15, "Fruit Cup", "Snack", 5.50, 2.00, 130),
]

staff = [
    (1, "James", "Wilson", "Store Manager", 1, "2022-01-15", 35.00),
    (2, "Emma", "Taylor", "Supervisor", 1, "2023-03-10", 28.00),
    (3, "Daniel", "Brown", "Team Member", 1, "2024-01-05", 24.00),
    (4, "Mia", "Martin", "Team Member", 1, "2024-08-12", 24.00),
    (5, "Olivia", "Chen", "Store Manager", 2, "2022-06-20", 35.00),
    (6, "Lucas", "Li", "Supervisor", 2, "2024-02-01", 28.00),
    (7, "Sophia", "Wang", "Team Member", 2, "2024-04-15", 24.00),
    (8, "Ethan", "White", "Team Member", 2, "2025-01-20", 24.00),
    (9, "Michael", "Smith", "Store Manager", 3, "2023-01-10", 35.00),
    (10, "Sarah", "Johnson", "Supervisor", 3, "2024-03-20", 28.00),
    (11, "Noah", "Harris", "Team Member", 3, "2024-07-08", 24.00),
    (12, "Chloe", "Clark", "Team Member", 3, "2025-02-17", 24.00),
]

suppliers = [
    (1, "SA Fresh Produce", "Lettuce", 2, "orders@safresh.example"),
    (2, "Adelaide Poultry Co", "Chicken", 2, "sales@poultry.example"),
    (3, "Southern Beef Supply", "Beef", 3, "orders@beef.example"),
    (4, "Ocean Catch SA", "Salmon", 3, "sales@ocean.example"),
    (5, "Green Soy Foods", "Tofu", 2, "orders@soy.example"),
    (6, "Metro Beverage Supply", "Soft Drinks", 1, "sales@beverage.example"),
    (7, "Riverland Juice Co", "Orange Juice", 2, "orders@juice.example"),
    (8, "Bakery Partners", "Cookies", 2, "sales@bakery.example"),
    (9, "Fresh Fruit Direct", "Fruit", 2, "orders@fruit.example"),
    (10, "Packaging Hub SA", "Packaging", 4, "sales@packaging.example"),
]


# -----------------------------
# Random customer data
# -----------------------------
first_names = [
    "Lucas", "Sarah", "John", "Emily", "Michael", "David", "Amy", "Tom",
    "Grace", "Kevin", "Jessica", "Ryan", "Olivia", "Jack", "Emma",
    "James", "Sophia", "Daniel", "Mia", "Noah", "Lily", "Ethan"
]

last_names = [
    "Li", "Chen", "Smith", "Wang", "Brown", "Lee", "Zhang", "Wilson",
    "Liu", "Taylor", "Davis", "Johnson", "Martin", "White", "Harris"
]

suburbs = [
    "Adelaide", "Mawson Lakes", "Glenelg", "Norwood", "Prospect",
    "Unley", "Modbury", "Henley Beach", "Burnside", "North Adelaide"
]


def random_datetime():
    start = datetime(2025, 1, 1)
    date_value = start + timedelta(days=random.randint(0, 364))

    hour = random.choices(
        population=[10, 11, 12, 13, 14, 17, 18, 19, 20],
        weights=[4, 8, 20, 18, 8, 10, 14, 12, 6],
        k=1,
    )[0]

    return date_value.replace(
        hour=hour,
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )


# -----------------------------
# Connect to SQLite
# -----------------------------
if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Clear old practice data
    for table in [
        "OrderItems", "Orders", "Inventory", "Staff",
        "Customers", "Products", "Suppliers", "Stores"
    ]:
        cursor.execute(f"DELETE FROM {table}")

    # Insert fixed tables
    cursor.executemany(
        "INSERT INTO Stores VALUES (?, ?, ?, ?, ?)",
        stores
    )

    cursor.executemany(
        "INSERT INTO Products VALUES (?, ?, ?, ?, ?, ?)",
        products
    )

    cursor.executemany(
        "INSERT INTO Staff VALUES (?, ?, ?, ?, ?, ?, ?)",
        staff
    )

    cursor.executemany(
        "INSERT INTO Suppliers VALUES (?, ?, ?, ?, ?)",
        suppliers
    )

    # Create customers
    customers = []
    for customer_id in range(1, CUSTOMER_COUNT + 1):
        member_level = random.choices(
            ["Bronze", "Silver", "Gold"],
            weights=[45, 35, 20],
            k=1
        )[0]

        join_date = datetime(2023, 1, 1) + timedelta(
            days=random.randint(0, 900)
        )

        customers.append((
            customer_id,
            random.choice(first_names),
            random.choice(last_names),
            random.choice(["Male", "Female"]),
            random.randint(18, 68),
            random.choice(suburbs),
            "SA",
            member_level,
            join_date.strftime("%Y-%m-%d")
        ))

    cursor.executemany(
        "INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        customers
    )

    # Create inventory: 10 ingredients x 3 stores = 30 rows
    ingredients = [
        ("Lettuce", "kg", 20),
        ("Chicken", "kg", 25),
        ("Beef", "kg", 20),
        ("Salmon", "kg", 12),
        ("Tofu", "kg", 15),
        ("Soft Drinks", "cases", 10),
        ("Orange Juice", "cases", 8),
        ("Cookies", "boxes", 10),
        ("Fruit", "kg", 12),
        ("Packaging", "boxes", 15),
    ]

    inventory_rows = []
    inventory_id = 1

    for store_id in [1, 2, 3]:
        for ingredient, unit, minimum_level in ingredients:
            inventory_rows.append((
                inventory_id,
                store_id,
                ingredient,
                random.randint(5, 60),
                unit,
                minimum_level
            ))
            inventory_id += 1

    cursor.executemany(
        "INSERT INTO Inventory VALUES (?, ?, ?, ?, ?, ?)",
        inventory_rows
    )

    # Create orders and order items
    product_prices = {row[0]: row[3] for row in products}
    staff_by_store = {
        1: [1, 2, 3, 4],
        2: [5, 6, 7, 8],
        3: [9, 10, 11, 12]
    }

    orders = []
    order_items = []
    order_item_id = 1

    for order_number in range(ORDER_COUNT):
        order_id = 1001 + order_number
        customer_id = random.randint(1, CUSTOMER_COUNT)
        store_id = random.choices([1, 2, 3], weights=[48, 30, 22], k=1)[0]
        staff_id = random.choice(staff_by_store[store_id])
        order_date = random_datetime().strftime("%Y-%m-%d %H:%M:%S")
        payment_method = random.choices(
            ["Card", "Cash", "Mobile"],
            weights=[65, 15, 20],
            k=1
        )[0]

        item_count = random.choices(
            [1, 2, 3, 4],
            weights=[25, 40, 25, 10],
            k=1
        )[0]

        selected_products = random.sample(
            range(1, 16),
            k=item_count
        )

        total_amount = 0

        for product_id in selected_products:
            quantity = random.choices([1, 2], weights=[85, 15], k=1)[0]
            unit_price = product_prices[product_id]
            total_amount += quantity * unit_price

            order_items.append((
                order_item_id,
                order_id,
                product_id,
                quantity,
                unit_price
            ))
            order_item_id += 1

        orders.append((
            order_id,
            customer_id,
            store_id,
            staff_id,
            order_date,
            payment_method,
            round(total_amount, 2)
        ))

    cursor.executemany(
        "INSERT INTO Orders VALUES (?, ?, ?, ?, ?, ?, ?)",
        orders
    )

    cursor.executemany(
        "INSERT INTO OrderItems VALUES (?, ?, ?, ?, ?)",
        order_items
    )

    conn.commit()

    print("Data generation complete.")
    print("Customers:", len(customers))
    print("Products:", len(products))
    print("Stores:", len(stores))
    print("Staff:", len(staff))
    print("Orders:", len(orders))
    print("OrderItems:", len(order_items))
    print("Inventory:", len(inventory_rows))
    print("Suppliers:", len(suppliers))

except Exception as error:
    conn.rollback()
    print("Error:", error)

finally:
    conn.close()
