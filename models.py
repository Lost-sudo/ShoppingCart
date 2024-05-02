import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='johnpatrick123',
    database='shoppingcart'
)

cursor = conn.cursor()

my_items = [
    # ('Hotdog', 100, 10),
    # ('Tocino Roll', 150, 10),
    # ('Meat', 250, 10),
    # ('Chicken', 200, 10),
    # ('Egg', 10, 1000),
    ('Suka', 12, 1000),
    ('Toyo', 13, 1000)
]

for item in my_items:
    cursor.execute('INSERT INTO items (item_name, price, quantity) VALUES (%s, %s, %s)', item)

conn.commit()
conn.close()


# import mysql.connector


# def create_cart_table():
#     try:
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='johnpatrick123',
#             database='shoppingcart'
#         )

#         cursor = conn.cursor()

#         # Create the cart table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS cart (
#                 cart_id INT AUTO_INCREMENT PRIMARY KEY,
#                 user_id INT,
#                 item_id INT,
#                 quantity INT,
#                 FOREIGN KEY (user_id) REFERENCES users(id),
#                 FOREIGN KEY (item_id) REFERENCES items(iditems)
#             )
#         """)

#         conn.commit()
#         print("Cart table created successfully")

#     except mysql.connector.Error as e:
#         print(f"Error creating cart table: {e}")

#     finally:
#         cursor.close()
#         conn.close()


# # Call the function to create the cart table
# create_cart_table()
