import sqlite3

conn = sqlite3.connect("../Database/FreshBowl.db")

cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM Customers
""")

result = cursor.fetchone()

print("Customers:", result[0])

conn.close()
