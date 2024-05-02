import customtkinter as ctk
from tkinter import messagebox
import traceback

from PIL import Image, ImageTk

import mysql.connector

from decimal import Decimal

from datetime import datetime

import qrcode
import uuid

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class MainApp:
    def __init__(self, master):
        self.master = master

        master.title("Shopping Cart")
        master.geometry("800x500")

        self.login = Login(master, self)
        self.login.pack(fill='both', expand=True)
        self.register = None

    def open_register_frame(self):
        if self.login:
            self.login.pack_forget()
        self.register = Register(self.master, self)
        self.register.pack(fill='both', expand=True)

    def open_login_frame(self):
        if self.register:
            self.register.pack_forget()
        self.login = Login(self.master, self)
        self.login.pack(fill='both', expand=True)

    def logout(self):
        for window in self.master.winfo_children():
            window.destroy()


class Login(ctk.CTkFrame):
    def __init__(self, login, main_app):
        super().__init__(login)
        self.main_app = main_app
        self.create_login_form()

    def create_login_form(self):
        self.login_frame = ctk.CTkFrame(master=self, width=320, height=360)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.login_label = ctk.CTkLabel(master=self.login_frame, text="Login to your account", font=('times', 20, 'bold'))
        self.login_label.place(x=50, y=45)

        self.username_label = ctk.CTkLabel(master=self.login_frame, text="Enter username")
        self.username_label.place(x=50, y=100)

        self.username_entry = ctk.CTkEntry(master=self.login_frame, width=220, font=("times new roman", 12))
        self.username_entry.place(x=50, y=120)

        self.password_label = ctk.CTkLabel(master=self.login_frame, text="Enter password")
        self.password_label.place(x=50, y=160)

        self.password_entry = ctk.CTkEntry(master=self.login_frame, width=220, font=("times new roman", 12), show='*')
        self.password_entry.place(x=50, y=180)

        self.login_btn = ctk.CTkButton(master=self.login_frame, text="Login", width=220, height=30, command=self.login_user)
        self.login_btn.place(x=50, y=240)

        self.register_btn_label = ctk.CTkLabel(master=self.login_frame, text="Don't have an account? Click here!", cursor="hand2")
        self.register_btn_label.place(x=50, y=280)
        self.register_btn_label.bind("<Button-1>", self.open_register_frame)

    def open_register_frame(self, _=None):
        self.main_app.open_register_frame()

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='johnpatrick123',
            database='shoppingcart'
        )

        cursor = conn.cursor()

        cursor.execute("SELECT id, shoppingcart FROM users WHERE username = %s and password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            user_id, shoppingcart = user
            self.main_app.current_user_id = user_id
            self.master.withdraw()
            ShoppingCart(master=self.master, main_app=self.main_app)
        else:
            messagebox.showerror("Error", "Invalid username or password")

        conn.close()
        cursor.close()



class Register(ctk.CTkFrame):
    def __init__(self, register, main_app):
        super().__init__(register)
        self.main_app = main_app
        self.create_registration_form()

    def create_registration_form(self):
        self.register_frame = ctk.CTkFrame(master=self, width=320, height=360)
        self.register_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.register_label = ctk.CTkLabel(master=self.register_frame, text="Register", font=('times new roman', 20, 'bold'))
        self.register_label.place(x=50, y=45)

        self.username_label = ctk.CTkLabel(master=self.register_frame, text="Enter username")
        self.username_label.place(x=50, y=100)

        self.username_entry = ctk.CTkEntry(master=self.register_frame, width=220, font=('times new roman', 12))
        self.username_entry.place(x=50, y=120)

        self.password_label = ctk.CTkLabel(master=self.register_frame, text="Enter password")
        self.password_label.place(x=50, y=160)

        self.password_entry = ctk.CTkEntry(master=self.register_frame, width=220, font=('times new roman', 12))
        self.password_entry.place(x=50, y=180)

        self.password_label2 = ctk.CTkLabel(master=self.register_frame, text="Confirm password")
        self.password_label2.place(x=50, y=210)

        self.password_entry2 = ctk.CTkEntry(master=self.register_frame, width=220, font=('times new roman', 12))
        self.password_entry2.place(x=50, y=230)

        self.register_btn = ctk.CTkButton(master=self.register_frame, text="Register", width=220, command=self.register_user)
        self.register_btn.place(x=50, y=280)

        self.register_btn_label = ctk.CTkLabel(master=self.register_frame, text="Already have an account? Click here!", cursor="hand2")
        self.register_btn_label.place(x=50, y=320)
        self.register_btn_label.bind("<Button-1>", self.open_login_frame)

    def open_login_frame(self, _=None):
        self.main_app.open_login_frame()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password2 = self.password_entry2.get()

        if password != password2:
            messagebox.showerror("Error", "Password do not match")
        else:
            if username and password:
                try:
                    conn = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='johnpatrick123',
                        database='shoppingcart'
                    )

                    cursor = conn.cursor()

                    shoppingcart = f"user_{username}"

                    cursor.execute("INSERT INTO users (username, password, shoppingcart) VALUES (%s, %s, %s)",
                                   (username, password, shoppingcart))

                    cursor.execute("INSERT INTO wallet (user_id, balance) VALUES (%s, %s)", (cursor.lastrowid, 0))

                    conn.commit()

                    cursor.close()
                    conn.close()

                    messagebox.showinfo("Success", "Registered successfully")

                    self.main_app.open_login_frame()

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Database error: {e}")
                    print(e)
            else:
                messagebox.showerror("Error", "Please fill out the form")


class ShoppingCart(ctk.CTkToplevel):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.master = master
        self.main_app = main_app

        self.title("Shopping Cart")
        self.geometry("1920x1080")
        self.resizable(True, True)

        self.create_widgets()

    def create_widgets(self):
        self.create_navbar()
        self.create_products_window()

    def create_navbar(self):
        self.navbar = ctk.CTkFrame(master=self)
        self.navbar.pack(fill='both', side='top')

        self.shopping_cart = ctk.CTkLabel(master=self.navbar, text="Welcome", font=("times new roman", 20, 'bold'))
        self.shopping_cart.pack(side='left', fill='x', expand=True)

        self.create_navbar_button("Cart", self.open_cart_window)
        self.create_navbar_button("Account", self.open_account_window)

    def create_navbar_button(self, text, command):
        button = ctk.CTkButton(master=self.navbar, text=text, command=command, fg_color="transparent")
        button.pack(side='left', fill='x', expand=True)

    def create_products_window(self):
        self.products_window = Products(master=self, main_app=self.main_app)
        self.products_window.pack(fill='both', expand=True, anchor='n')

    def open_cart_window(self):
        Cart(master=self.master, main_app=self.main_app)

    def open_account_window(self):
        Account(master=self.master, main_app=self.main_app)


class Products(ctk.CTkFrame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app

        self.frame = ctk.CTkFrame(master=master)
        self.frame.pack(fill='x', side='top', anchor='n')

        self.products_frame = ctk.CTkFrame(master=master)
        self.products_frame.pack(fill='both', anchor='n')

        self.frame1 = ctk.CTkFrame(master=self.frame, height=100, width=50)
        self.frame1.pack(fill='both', side='top')

        self.shop_owner_label = ctk.CTkLabel(master=self.frame1, text="John Patrick's Shop", font=("times new roman", 20, 'bold'))
        self.shop_owner_label.pack(fill='x', expand=True)

        self.labels = []
        self.quantity_labels = []
        self.quantity_entries = []
        self.add_to_cart_buttons = []
        self.buy_now_buttons = []

        self.initialize_widgets()
        self.get_items()
        self.item_quantity()

    def initialize_widgets(self):
        image_width = 200
        image_height = 200

        items = [
            {"name": "Hotdog", "image_path": "images/hotdog.jpg", "id": 1},
            {"name": "Tocino", "image_path": "images/tocinojpg.jpg", "id": 2},
            {"name": "Meat", "image_path": "images/meat.jpg", "id": 3},
            {"name": "Chicken", "image_path": "images/chickenjpg.jpg", "id": 4},
            {"name": "Egg", "image_path": "images/egg.jpg", "id": 5},
            {"name": "Suka", "image_path": "images/suka.jpg", "id": 6},
            {"name": "Toyo", "image_path": "images/babaji.jpg", "id": 7}
        ]

        for item in items:
            label_frame = ctk.CTkFrame(master=self.products_frame, height=100, width=100)
            label_frame.pack(side='left', fill='x', pady=10, padx=10)

            item_image = Image.open(item["image_path"]).resize((image_width, image_height))
            item_ctk_image = ctk.CTkImage(light_image=item_image, dark_image=item_image,
                                           size=(image_width, image_height))
            item_label = ctk.CTkLabel(master=label_frame, image=item_ctk_image, text="")
            item_label.pack(fill='both')

            item_name_label = ctk.CTkLabel(master=label_frame, font=("times new roman", 15), text='')
            item_name_label.pack(fill='x')
            self.labels.append(item_name_label)

            # item_quantity_label = ctk.CTkLabel(master=label_frame, font=("times new roman", 15), text='')
            # item_quantity_label.pack(fill='x')
            # self.quantity_labels.append(item_quantity_label)

            item_quantity_entry = ctk.CTkEntry(master=label_frame, font=("times new roman", 15))
            item_quantity_entry.pack(fill='x')
            self.quantity_entries.append(item_quantity_entry)

            add_to_cart_button = ctk.CTkButton(master=label_frame, text="Add to cart", font=("times new roman", 15),
                                                command=lambda idx=item["id"]: self.add_to_cart(idx, int(self.quantity_entries[idx - 1].get())))
            add_to_cart_button.pack(fill='x')

            buy_now_button = ctk.CTkButton(master=label_frame, text="Buy now", font=("times new roman", 15),
                                            command=lambda idx=item["id"]: self.buy_now(idx, int(self.quantity_entries[idx - 1].get())))
            buy_now_button.pack(fill='x', side='bottom')

            self.add_to_cart_buttons.append(add_to_cart_button)
            self.buy_now_buttons.append(buy_now_button)

    def database_connect(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='johnpatrick123',
            database='shoppingcart'
        )

    def database_disconnect(self, conn, cursor):
        cursor.close()
        conn.close()

    def buy_now(self, item_id, quantity):
        user_id = self.main_app.current_user_id
        quantity = int(self.quantity_entries[item_id - 1].get())
        user_id = self.main_app.current_user_id

        conn = self.database_connect()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT item_name, price FROM items WHERE iditems = %s", (item_id,))
            item = cursor.fetchone()
            item_name, item_price = item

            total_price = item_price * quantity

            confirm_window = ctk.CTkToplevel(self)
            confirm_window.title("Confirm Purchase")
            confirm_window.geometry("400x200")

            confirm_label = ctk.CTkLabel(confirm_window,
                                         text=f"Item: {item_name}\nQuantity: {quantity}\nTotal Price: ₱{total_price}\n\nConfirm Purchase?",
                                         font=("times new roman", 12))
            confirm_label.pack(pady=20)

            def confirm_purchase():
                confirm_window.destroy()
                conn = self.database_connect()

                cursor = conn.cursor()

                cursor.execute("SELECT balance FROM wallet WHERE user_id = %s", (user_id,))
                balance = cursor.fetchone()[0]

                if balance < total_price:
                    messagebox.showerror("ERROR", "Insufficient balance")
                    return

                new_balance = balance - total_price
                cursor.execute("UPDATE wallet SET balance = %s WHERE user_id = %s", (new_balance, user_id))

                transaction_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO purchase_history (user_id, total_price, transaction_id) VALUES (%s, %s, %s)",
                    (user_id, total_price, transaction_id))

                conn.commit()

                receipt_text = f"Transaction ID: {transaction_id}\n"
                receipt_text += f"Item: {item_name}\n"
                receipt_text += f"Quantity: {quantity}\n"
                receipt_text += f"Total Price: ₱{total_price}\n"

                messagebox.showinfo("SUCCESS", "Purchase successful\n\nReceipt:\n\n" + receipt_text)


            confirm_button = ctk.CTkButton(confirm_window, text="Confirm", command=confirm_purchase)
            confirm_button.pack()
            
            self.database_disconnect(conn, cursor)
        except mysql.connector.Error as e:
            conn.rollback()
            messagebox.showerror("ERROR", "Database Error {}".format(e))

    def get_items(self):
            conn = self.database_connect()

            cursor = conn.cursor()

            cursor.execute("SELECT item_name, price FROM items")
            result = cursor.fetchall()

            for idx, (item_name, price) in enumerate(result):
                label_text = "{}\nPrice: ₱{}".format(item_name, price)
                self.labels[idx].configure(text=label_text)

            self.database_disconnect(conn, cursor)
    def item_quantity(self):
            conn = self.database_connect()

            cursor = conn.cursor()

            cursor.execute("SELECT quantity FROM items")
            result = cursor.fetchall()

            for idx, (quantity,) in enumerate(result):
                _quantity = "Quantity: {}".format(quantity)
                self.quantity_labels[idx].configure(text=_quantity)

            self.database_disconnect(conn, cursor)

    def add_to_cart(self, item_id, quantity):
        user_id = self.main_app.current_user_id
        quantity = int(self.quantity_entries[item_id - 1].get())
        user_id = self.main_app.current_user_id

        conn = self.database_connect()

        cursor = conn.cursor()

        cursor.execute("SELECT quantity FROM cart WHERE user_id = %s AND item_id = %s",
                       (user_id, item_id))
        result = cursor.fetchone()

        if result:
            new_quantity = result[0] + quantity
            cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND item_id = %s",
                           (new_quantity, user_id, item_id))
        else:
            cursor.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (%s, %s, %s)",
                           (user_id, item_id, quantity))

        conn.commit()
        self.database_disconnect(conn, cursor)
        messagebox.showinfo("SUCCESS", "Item added to cart")


class Cart(ctk.CTkToplevel):
    def __init__(self, master, main_app):
        super().__init__(master)

        self.main_app = main_app

        self.title("CART")
        self.geometry("500x500")

        self.create_widgets()

        self.display_cart_items()
        self.calculate_total_price()
        self.wallet_balance()

        self.transient(master)
        self.grab_set()
        self.focus_force()

    def create_widgets(self):
        self.label1 = ctk.CTkLabel(master=self, text="CART", font=("times new roman", 20, 'bold'))
        self.label1.pack(fill='x', anchor='center')

        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(fill='both', expand=True)

        self.total_frame = ctk.CTkFrame(master=self.frame)
        self.total_frame.pack(fill='x', side='top')

        self.wallet_balance_frame = ctk.CTkFrame(master=self.frame)
        self.wallet_balance_frame.pack(fill='x', side='top')

        self.check_out_frame = ctk.CTkFrame(master=self.frame)
        self.check_out_frame.pack(fill='x', side='bottom')

        self.payment_method = ctk.StringVar()
        self.payment_method.set("wallet_balance")

        self.total_label = ctk.CTkLabel(master=self.total_frame, text="Total Price: ", font=("times new roman", 15))
        self.total_label.pack(side='left')

        self.total_value_label = ctk.CTkLabel(master=self.total_frame, text="", font=("times new roman", 15))
        self.total_value_label.pack(side='right')

        self.total_label = ctk.CTkLabel(master=self.wallet_balance_frame, text="Wallet Balance: ",
                                        font=("times new roman", 15))
        self.total_label.pack(side='left')

        self.wallet_balance_label = ctk.CTkLabel(master=self.wallet_balance_frame, text="",
                                                 font=('times new roman', 15))
        self.wallet_balance_label.pack(side='left')

        self.payment_options = [
            ("Wallet Balance", "wallet_balance"),
            ("Online Payment (QR Code)", "online_payment"),
            ("Cash", "cash")
        ]

        for text, method in self.payment_options:
            ctk.CTkRadioButton(master=self.check_out_frame, text=text, variable=self.payment_method, value=method).pack(
                anchor='w')

        self.check_out = ctk.CTkButton(master=self.check_out_frame, text="Check Out", font=("times new roman", 15),
                                       command=self.check_out_process)
        self.check_out.pack(side='right')

    def database_connect(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='johnpatrick123',
            database='shoppingcart'
        )

    def database_disconnect(self, conn, cursor):
        cursor.close()
        conn.close()

    def display_cart_items(self):
        user_id = self.main_app.current_user_id

        conn = self.database_connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT items.item_name, items.price, cart.quantity FROM items INNER JOIN cart ON items.iditems = cart.item_id WHERE cart.user_id = %s",
            (user_id,))
        cart_items = cursor.fetchall()

        for idx, (item_name, price, quantity) in enumerate(cart_items, start=1):
            item_label = ctk.CTkLabel(master=self.frame, text=f"{item_name} - P{price} - Quantity: {quantity}")
            item_label.pack(fill='x', pady=5)

        if not cart_items:
            empty_label = ctk.CTkLabel(master=self.frame, text="Your cart is empty")
            empty_label.pack(fill='x', pady=5)

        self.database_disconnect(conn, cursor)

    def calculate_total_price(self):
        user_id = self.main_app.current_user_id

        conn = self.database_connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT SUM(items.price * cart.quantity) FROM items INNER JOIN cart ON items.iditems = cart.item_id WHERE cart.user_id = %s",
            (user_id,))
        total_price = cursor.fetchone()[0]

        self.total_value_label.configure(
            text="₱{}".format(total_price))

        self.database_disconnect(conn, cursor)


    def wallet_balance(self):
        user_id = self.main_app.current_user_id

        conn = self.database_connect()

        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM wallet WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            balance_str = str(result[0])
            balance_str = balance_str.replace("(", "").replace(")", "").replace(",", "")
            self.wallet_balance_label.configure(
                text="₱{}".format(balance_str)
            )
        else:
            self.wallet_balance_label.configure(
                text="₱0"
            )

        self.database_disconnect(conn, cursor)

    def check_out_process(self):
        total_price_str = self.total_value_label.cget("text").replace("₱", "")
        user_id = self.main_app.current_user_id
        payment_method = self.payment_method.get()

        payment_successful = False

        if payment_method == "wallet_balance":
            payment_successful = self.pay_with_wallet(total_price_str, user_id)
        elif payment_method == "online_payment":
            payment_successful = self.pay_online(total_price_str, user_id)
        elif payment_method == "cash":
            payment_successful = self.pay_with_cash(total_price_str, user_id)

        if payment_successful:
            self.empty_cart(user_id)

    def pay_with_wallet(self, total_price_str, user_id):

        transaction_id = str(uuid.uuid4())

        total_price = Decimal(total_price_str.replace('₱', ''))
        user_id = self.main_app.current_user_id

        conn = self.database_connect()

        cursor = conn.cursor()

        try:
            conn.start_transaction()

            cursor.execute("SELECT balance FROM wallet WHERE user_id = %s FOR UPDATE", (user_id,))
            balance = cursor.fetchone()[0]
            new_balance = balance - total_price

            if new_balance < total_price:
                messagebox.showerror("ERROR", "Insufficient balance")
                return False

            cursor.execute("UPDATE wallet SET balance = %s WHERE user_id = %s", (new_balance, user_id))

            cursor.execute("INSERT INTO purchase_history (user_id, total_price, transaction_id) VALUES (%s, %s, %s)",
                           (user_id, total_price, transaction_id))

            conn.commit()

            messagebox.showinfo("SUCCESS", "Payment successful")
            return True

        except mysql.connector.Error as e:
            conn.rollback()
            messagebox.showerror("ERROR", e)
            return False

        finally:
            self.database_disconnect(conn, cursor)

    def pay_online(self, total_price_str, user_id):
        pay_online_window = ctk.CTkToplevel(self)
        pay_online_window.title("Online Payment")
        pay_online_window.geometry("400x400")

        transaction_id = str(uuid.uuid4())

        total_price = Decimal(total_price_str.replace('₱', ''))

        payment_data = f'Your payment data: {user_id} - {total_price} - {transaction_id}'

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(payment_data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        qr_image_tk = ImageTk.PhotoImage(qr_image)

        qr_label = ctk.CTkLabel(master=pay_online_window, image=qr_image_tk, text="")
        qr_label.image = qr_image_tk
        qr_label.pack(fill='both', expand=True)

        def confirm_payment():
            conn = self.database_connect()

            cursor = conn.cursor()

            try:
                conn.start_transaction()

                cursor.execute(
                    "INSERT INTO purchase_history (user_id, total_price, transaction_id) VALUES (%s, %s, %s)",
                    (user_id, total_price, transaction_id))
                conn.commit()

                messagebox.showinfo("SUCCESS", "Payment successful")
                return True

            except mysql.connector.Error as e:
                conn.rollback()
                messagebox.showerror("ERROR", e)
                return False

            finally:
                self.database_disconnect(conn, cursor)

        payment_done = ctk.CTkButton(master=pay_online_window, text="Done Payment", font=("times new roman", 15),
                                     command=confirm_payment)
        payment_done.pack(side='bottom')

    def pay_with_cash(self, total_price_str, user_id):
        pay_cash_window = ctk.CTkToplevel(self)
        pay_cash_window.title("Cash Payment")

        transaction_id = str(uuid.uuid4())

        total_price = Decimal(total_price_str.replace('₱', ''))
        user_id = self.main_app.current_user_id

        amount_paid = ctk.CTkLabel(master=pay_cash_window, text="Cash Amount", font=('times new roman', 15))
        amount_paid.pack()

        amount_paid_entry = ctk.CTkEntry(master=pay_cash_window, font=("times new roman", 15))
        amount_paid_entry.pack()

        def confirm_payment():
            cash_amount_str = amount_paid_entry.get()
            cash_amount = Decimal(cash_amount_str) if cash_amount_str else Decimal(0)

            change = cash_amount - total_price
            if change < 0:
                messagebox.showerror("ERROR", "Insufficient cash amount.")
                return False
            messagebox.showinfo("Change", f"Change: ₱{change}")
            conn = self.database_connect()

            cursor = conn.cursor()

            try:
                conn.start_transaction()

                cursor.execute(
                    "INSERT INTO purchase_history (user_id, total_price, transaction_id) VALUES (%s, %s, %s)",
                    (user_id, total_price, transaction_id))
                conn.commit()

                purchased_items = []
                for item in self.cart_items:
                    purchased_items.append(f"{item['name']} - Quantity: {item['quantity']}")

                receipt_message = f"Purchase successful!\n\n"
                receipt_message += f"Date: {datetime.now()}\n"
                receipt_message += f"Items purchased:\n"
                receipt_message += "\n".join(purchased_items)

                messagebox.showinfo("SUCCESS", "Payment successful")
                pay_cash_window.destroy()
                return True

            except mysql.connector.Error as e:
                conn.rollback()
                messagebox.showerror("ERROR", e)
                return False

            finally:
                self.database_disconnect(conn, cursor)
        confirm_payment_button = ctk.CTkButton(master=pay_cash_window, text="Confirm Payment",
                                               font=("times new roman", 15), command=confirm_payment)
        confirm_payment_button.pack()


    def empty_cart(self, user_id):
        conn = self.database_connect()

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
            conn.commit()
        except mysql.connector.Error as e:
            conn.rollback()
            messagebox.showerror("ERROR", e)
        finally:
            self.database_disconnect(conn, cursor)


class Account(ctk.CTkToplevel):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.title("ACCOUNT")
        self.geometry("500x500")
        self.main_app = main_app
        self.create_widgets()
        self.get_wallet_balance()
        self.transient(master)
        self.grab_set()
        self.focus_force()

    def create_widgets(self):
        self.label1 = ctk.CTkLabel(master=self, text="ACCOUNT", font=("times new roman", 20, 'bold'))
        self.label1.pack(fill='x', anchor='center')

        self.frame1 = ctk.CTkFrame(master=self)
        self.frame1.pack(fill='both', expand=True)

        self.account_balance_label = ctk.CTkLabel(master=self.frame1, text='', font=("times new roman", 50))
        self.account_balance_label.pack(anchor='center')

        self.add_balance_btn = ctk.CTkButton(master=self.frame1, text="Add Balance", font=("times new roman", 15),
                                             command=self.add_balance)
        self.add_balance_btn.pack(anchor='center', padx=50, pady=50)

        self.purchase_history_btn = ctk.CTkButton(master=self.frame1, text="Purchase History",
                                                  font=("times new roman", 15), command=self.purchase_history)
        self.purchase_history_btn.pack(anchor='center', padx=50, pady=50)

        self.logout_btn = ctk.CTkButton(master=self.frame1, text="Logout", font=("times new roman", 15),
                                        command=self.logout)
        self.logout_btn.pack(anchor='center', padx=50, pady=50)

    def database_connect(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='johnpatrick123',
            database='shoppingcart'
        )

    def database_disconnect(self, conn, cursor):
        cursor.close()
        conn.close()



    def get_wallet_balance(self):
        user_id = self.main_app.current_user_id

        conn = self.database_connect()

        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM wallet WHERE user_id = %s", (user_id,))
        wallet = cursor.fetchone()

        if wallet:
            balance_str = str(wallet[0])
            balance_str = balance_str.replace("(", "").replace(")", "").replace(",", "")
            self.account_balance_label.configure(
                text="₱{}".format(balance_str)
            )
        else:
            self.account_balance_label.configure(
                text="₱0"
            )

        self.database_disconnect(conn, cursor)

    def add_balance(self):
        add_balance_window = ctk.CTkToplevel(self)
        add_balance_window.title("ADD BALANCE")
        add_balance_window.geometry("500x500")

        user_id = self.main_app.current_user_id

        enter_amount = ctk.CTkLabel(master=add_balance_window, text="Enter amount to add to balance",
                                    font=("times new roman", 15))
        enter_amount.pack(anchor='center')

        enter_amount_entry = ctk.CTkEntry(master=add_balance_window, font=("times new roman", 15))
        enter_amount_entry.pack(anchor='center')

        def confirm_add_balance():
            amount = enter_amount_entry.get()

            if not amount.isdigit():
                messagebox.showerror("ERROR", "Invalid amount")
                return

            try:
                conn = self.database_connect()

                cursor = conn.cursor()

                cursor.execute("UPDATE wallet SET balance = balance + %s WHERE user_id = %s", (float(amount), user_id))

                conn.commit()

                self.database_disconnect(conn, cursor)

                messagebox.showinfo("SUCCESS", "Balance added")

            except Exception as e:
                print("Error:", e)
                traceback.print_exc()
                messagebox.showerror("ERROR", "An error occurred while adding balance. Please try again later.")

        confirm_amount_entry = ctk.CTkButton(master=add_balance_window, text="Confirm", font=("times new roman", 15),
                                             command=confirm_add_balance)
        confirm_amount_entry.pack(anchor='center')

    def purchase_history(self):
        purchase_history_window = ctk.CTkToplevel(self)
        purchase_history_window.title("PURCHASE HISTORY")
        purchase_history_window.geometry("500x500")

        purchase_history_label = ctk.CTkLabel(purchase_history_window, text="", font=('times new roman', 15))
        purchase_history_label.pack(anchor='center')

        self.grab_set()
        self.focus_force()

        user_id = self.main_app.current_user_id
 
        conn = self.database_connect()

        cursor = conn.cursor()

        cursor.execute("SELECT purchase_date, total_price, transaction_id FROM purchase_history WHERE user_id = %s",
                       (user_id,))
        purchase_history = cursor.fetchall()

        history_text = ""

        for purchase_date, total_price, transaction_id in purchase_history:
            history_text += f"{purchase_date} - ₱{total_price} - {transaction_id}\n"

        purchase_history_label.configure(text=history_text)

        self.database_disconnect(conn, cursor)

    def logout(self):
        self.main_app.logout()
        self.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
