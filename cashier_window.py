import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from datetime import datetime
from database import Database


class CashierWindow:
    def __init__(self, user_id, name, cashier_id):
        self.root = tk.Tk()
        self.root.title(f"Nabunturan POS - Cashier: {name}")
        self.root.geometry("1200x750")
        self.root.state('zoomed')  # Maximize window
        self.db = Database()
        self.user_id = user_id
        self.cashier_id = cashier_id
        self.cashier_name = name
        self.cart = []
        self.selected_product_in_tree = None
        self.discount = 0.0

        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#e0e0e0')
        self.style.configure('TLabel', background='#e0e0e0')
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        self.style.map('TButton',
                       foreground=[('active', 'black')],
                       background=[('active', '#cccccc')])
        self.style.configure('Treeview', rowheight=25, font=('Arial', 10))
        self.style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))

        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

        # Left Navigation Panel
        nav_frame = tk.Frame(main_frame, width=220, bg='#2c3e50')
        nav_frame.pack(side='left', fill='y', padx=(0, 10))
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="CASHIER PANEL", font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white').pack(
            pady=(20, 5))
        tk.Label(nav_frame, text=name, font=('Arial', 10), bg='#2c3e50', fg='white').pack(pady=(0, 20))

        # Navigation Buttons
        self.current_view = tk.StringVar(value='pos')

        self.btn_dashboard = tk.Button(nav_frame, text="Dashboard", command=lambda: self.show_view('dashboard'),
                                       bg='#34495e', fg='white', font=('Arial', 10, 'bold'), relief='flat', padx=10,
                                       pady=10)
        self.btn_dashboard.pack(fill='x', pady=5, padx=10)
        self.btn_pos = tk.Button(nav_frame, text="Point of Sale", command=lambda: self.show_view('pos'),
                                 bg='#1abc9c', fg='white', font=('Arial', 10, 'bold'), relief='flat', padx=10,
                                 pady=10)
        self.btn_pos.pack(fill='x', pady=5, padx=10)
        self.btn_shift_report = tk.Button(nav_frame, text="Shift Report",
                                          command=lambda: self.show_view('shift_report'),
                                          bg='#34495e', fg='white', font=('Arial', 10, 'bold'), relief='flat', padx=10,
                                          pady=10)
        self.btn_shift_report.pack(fill='x', pady=5, padx=10)

        # Logout button
        logout_btn_nav = tk.Button(nav_frame, text="Logout", command=self.logout,
                                   bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), relief='flat', padx=10,
                                   pady=10)
        logout_btn_nav.pack(fill='x', pady=(50, 10), padx=10, side='bottom')

        # Right Content Area
        self.content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.content_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Initialize last sale variables
        self.last_sale_id = None
        self.last_payment_method = None
        self.last_final_total = 0.0
        self.last_amount_tendered = 0.0
        self.last_change = 0.0
        self.last_cart_items = []

        # Show POS view initially
        self.show_view('pos')

        # Start the main loop
        self.root.mainloop()

    def clear_content_frame(self):
        if hasattr(self, 'content_frame') and self.content_frame.winfo_exists():
            for widget in self.content_frame.winfo_children():
                widget.destroy()

    def show_view(self, view_name):
        self.clear_content_frame()
        self.current_view.set(view_name)
        self.btn_dashboard.config(bg='#34495e')
        self.btn_pos.config(bg='#34495e')
        self.btn_shift_report.config(bg='#34495e')

        if view_name == 'dashboard':
            self.btn_dashboard.config(bg='#1abc9c')
            self.setup_dashboard_view()
        elif view_name == 'pos':
            self.btn_pos.config(bg='#1abc9c')
            self.setup_pos_view()
        elif view_name == 'shift_report':
            self.btn_shift_report.config(bg='#1abc9c')
            self.setup_shift_report_view()

    def setup_dashboard_view(self):
        """Setup cashier dashboard with performance metrics"""
        # Title
        title_font = font.Font(family="Arial", size=18, weight="bold")
        header_font = font.Font(family="Arial", size=13, weight="bold")
        normal_font = font.Font(family="Arial", size=10)
        card_value_font = font.Font(family="Arial", size=28, weight="bold")

        title_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', pady=(0, 20))

        tk.Label(title_frame, text="My Dashboard", font=title_font, bg='#f0f0f0', fg='#2c3e50').pack(side='left', padx=10)
        tk.Label(title_frame, text=f"Shift Date: {datetime.now().strftime('%Y-%m-%d')}",
                 font=normal_font, bg='#f0f0f0', fg='#7f8c8d').pack(side='right', padx=10)

        # Get cashier stats for today
        stats = self.get_cashier_daily_stats()

        # Summary cards
        card_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        card_frame.pack(fill='x', pady=(0, 20))

        card_data = [
            ("Total Sales", f"₱{stats['total_sales']:,.2f}", "#2ecc71", "💰"),
            ("Transactions", str(stats['transaction_count']), "#3498db", "📊"),
            ("Average Sale", f"₱{stats['average_sale']:,.2f}", "#f39c12", "📈"),
            ("Total Items Sold", str(stats['items_sold']), "#9b59b6", "📦"),
        ]

        for i, (title, value, color, icon) in enumerate(card_data):
            card = self.create_dashboard_card(card_frame, title, value, color, icon, header_font, card_value_font, normal_font)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

        for i in range(4):
            card_frame.grid_columnconfigure(i, weight=1)

        # Recent transactions
        trans_frame = tk.Frame(self.content_frame, bg='white', relief='ridge', bd=1)
        trans_frame.pack(fill='both', expand=True, pady=(0, 20))

        tk.Label(trans_frame, text="Your Transactions Today", font=header_font, bg='white', fg='#2c3e50').pack(
            anchor='w', padx=20, pady=(20, 10))

        # Create treeview
        columns = ("id", "time", "items", "total", "payment")
        tree = ttk.Treeview(trans_frame, columns=columns, show="headings", height=15)

        tree.heading("id", text="Receipt #")
        tree.heading("time", text="Time")
        tree.heading("items", text="Items")
        tree.heading("total", text="Total")
        tree.heading("payment", text="Payment Method")

        tree.column("id", width=80, anchor="center")
        tree.column("time", width=120, anchor="center")
        tree.column("items", width=80, anchor="center")
        tree.column("total", width=120, anchor="e")
        tree.column("payment", width=120, anchor="center")

        # Get transactions
        transactions = self.get_cashier_transactions()
        for trans in transactions:
            tree.insert("", tk.END, values=trans)

        scrollbar = ttk.Scrollbar(trans_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side=tk.LEFT, fill='both', expand=True, padx=20, pady=(0, 20))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=(0, 20))

    def create_dashboard_card(self, parent, title, value, color, icon, header_font, card_value_font, normal_font):
        """Create a dashboard card"""
        card = tk.Frame(parent, bg="white", relief=tk.SOLID, bd=1, padx=20, pady=20)

        # Icon and value
        top_frame = tk.Frame(card, bg="white")
        top_frame.pack(fill=tk.X, pady=(0, 10))

        icon_label = tk.Label(top_frame, text=icon, font=("Arial", 32), bg="white")
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        value_label = tk.Label(top_frame, text=value, font=card_value_font, bg="white", fg=color)
        value_label.pack(side=tk.LEFT)

        # Title
        title_label = tk.Label(card, text=title, font=header_font, bg="white", fg="#7f8c8d")
        title_label.pack(anchor="w")

        return card

    def get_cashier_daily_stats(self):
        """Get cashier's daily statistics"""
        # Total sales today
        sales_query = """
            SELECT COALESCE(SUM(total), 0), COUNT(*), COALESCE(AVG(total), 0)
            FROM sales
            WHERE cashier_id = %s AND DATE(date) = CURDATE() AND payment_method != 'report'
        """
        sales_result = self.db.execute_query(sales_query, (self.cashier_id,), fetch=True)

        if sales_result:
            total_sales = float(sales_result[0][0])
            transaction_count = int(sales_result[0][1])
            average_sale = float(sales_result[0][2])
        else:
            total_sales = 0.0
            transaction_count = 0
            average_sale = 0.0

        # Total items sold
        items_query = """
            SELECT COALESCE(SUM(quantity), 0)
            FROM sale_items si
            JOIN sales s ON si.sale_id = s.id
            WHERE s.cashier_id = %s AND DATE(s.date) = CURDATE() AND s.payment_method != 'report'
        """
        items_result = self.db.execute_query(items_query, (self.cashier_id,), fetch=True)
        items_sold = int(items_result[0][0]) if items_result else 0

        return {
            'total_sales': total_sales,
            'transaction_count': transaction_count,
            'average_sale': average_sale,
            'items_sold': items_sold
        }

    def get_cashier_transactions(self):
        """Get cashier's transactions for today"""
        query = """
            SELECT s.id, TIME_FORMAT(s.date, '%h:%i %p'), 
                   (SELECT COUNT(*) FROM sale_items WHERE sale_id = s.id),
                   s.total, s.payment_method
            FROM sales s
            WHERE s.cashier_id = %s AND DATE(s.date) = CURDATE() AND s.payment_method != 'report'
            ORDER BY s.date DESC
        """
        results = self.db.execute_query(query, (self.cashier_id,), fetch=True)

        if results:
            return [(row[0], row[1], int(row[2]), f"₱{float(row[3]):,.2f}", row[4].upper())
                    for row in results]
        return []

    def setup_shift_report_view(self):
        tk.Label(self.content_frame, text="Shift Report & Feedback", font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(
            pady=20)
        tk.Label(self.content_frame, text="Submit any issues or important notes from your shift.", bg='#f0f0f0').pack(
            pady=10)

        self.shift_report_text = scrolledtext.ScrolledText(self.content_frame, height=15, width=70)
        self.shift_report_text.pack(padx=20, pady=10)

        submit_btn = tk.Button(self.content_frame, text="Submit Shift Report", command=self.submit_shift_report,
                               bg='#9C27B0', fg='white')
        submit_btn.pack(pady=10)

    def submit_shift_report(self):
        feedback = self.shift_report_text.get(1.0, tk.END).strip()
        if not feedback:
            messagebox.showwarning("Warning", "Enter feedback for the report.")
            return

        report_query = "INSERT INTO sales (cashier_id, total, discount, payment_method, feedback) VALUES (%s, 0, 0, 'report', %s)"
        if self.db.execute_query(report_query, (self.cashier_id, feedback)):
            messagebox.showinfo("Success", "Shift Report submitted.")
            self.shift_report_text.delete(1.0, tk.END)
            log_query = "INSERT INTO cashier_logs (cashier_id, activity) VALUES (%s, 'Shift Report submitted')"
            self.db.execute_query(log_query, (self.cashier_id,))
        else:
            messagebox.showerror("Error", "Failed to submit report.")

    def setup_pos_view(self):
        # Title
        header_frame = tk.Frame(self.content_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(header_frame, text="Point of Sale", font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(
            side='left', padx=10)

        datetime_label = tk.Label(header_frame, text=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                  font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        datetime_label.pack(side='right', padx=10)

        # Main POS Container
        pos_container = tk.Frame(self.content_frame, bg='#f0f0f0')
        pos_container.pack(fill='both', expand=True)

        pos_container.grid_rowconfigure(0, weight=1)
        pos_container.grid_columnconfigure(0, weight=3)
        pos_container.grid_columnconfigure(1, weight=2)

        # LEFT SIDE: Product Panel
        product_frame = tk.Frame(pos_container, bg='white', relief='ridge', bd=2)
        product_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        search_header = tk.Frame(product_frame, bg='#3498db', height=50)
        search_header.pack(fill='x')

        tk.Label(search_header, text="🔍 Product Search", font=('Arial', 12, 'bold'),
                 bg='#3498db', fg='white').pack(side='left', padx=10, pady=10)

        search_frame = tk.Frame(product_frame, bg='white', pady=10)
        search_frame.pack(fill='x', padx=10)

        tk.Label(search_frame, text="Search:", bg='white', font=('Arial', 10)).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, width=30, font=('Arial', 11))
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_products())

        search_btn = tk.Button(search_frame, text="Search", command=self.search_products,
                               bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                               relief='flat', padx=15, pady=5)
        search_btn.pack(side='left', padx=5)

        clear_btn = tk.Button(search_frame, text="Clear", command=self.clear_search,
                              bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                              relief='flat', padx=15, pady=5)
        clear_btn.pack(side='left', padx=5)

        # Product treeview
        tree_frame = tk.Frame(product_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        product_cols = ('Seq', 'Product Name', 'Price', 'Stock')
        self.product_tree = ttk.Treeview(tree_frame, columns=product_cols, show='headings', height=18)

        self.product_tree.heading('Seq', text='ID')
        self.product_tree.column('Seq', width=60, anchor='center')

        self.product_tree.heading('Product Name', text='Product Name')
        self.product_tree.column('Product Name', width=280, anchor='w')

        self.product_tree.heading('Price', text='Price')
        self.product_tree.column('Price', width=100, anchor='center')

        self.product_tree.heading('Stock', text='Stock')
        self.product_tree.column('Stock', width=100, anchor='center')

        prod_vscroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.product_tree.yview)
        prod_hscroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.product_tree.xview)
        self.product_tree.configure(yscrollcommand=prod_vscroll.set, xscrollcommand=prod_hscroll.set)

        self.product_tree.grid(row=0, column=0, sticky='nsew')
        prod_vscroll.grid(row=0, column=1, sticky='ns')
        prod_hscroll.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Add to cart controls
        cart_control_frame = tk.Frame(product_frame, bg='#ecf0f1', pady=10)
        cart_control_frame.pack(fill='x', padx=10, pady=(5, 10))

        tk.Label(cart_control_frame, text="Quantity:", bg='#ecf0f1',
                 font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        self.qty_entry = tk.Entry(cart_control_frame, width=10, font=('Arial', 11))
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side='left', padx=5)

        add_btn = tk.Button(cart_control_frame, text="➕ Add to Cart", command=self.add_to_cart,
                            bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                            relief='flat', padx=20, pady=8)
        add_btn.pack(side='left', padx=10)

        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select_tree)
        self.product_tree.bind('<Double-1>', lambda e: self.add_to_cart())

        self.load_products()

        # RIGHT SIDE: Cart Panel
        cart_frame = tk.Frame(pos_container, bg='white', relief='ridge', bd=2)
        cart_frame.grid(row=0, column=1, sticky='nsew')

        cart_header = tk.Frame(cart_frame, bg='#e74c3c', height=50)
        cart_header.pack(fill='x')

        tk.Label(cart_header, text="🛒 Shopping Cart", font=('Arial', 12, 'bold'),
                 bg='#e74c3c', fg='white').pack(side='left', padx=10, pady=10)

        # Cart treeview - REDUCED HEIGHT to make room for buttons
        cart_tree_frame = tk.Frame(cart_frame, bg='white')
        cart_tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        cart_cols = ('Product ID', 'Product Name', 'Price', 'Qty', 'Subtotal')
        self.cart_tree = ttk.Treeview(cart_tree_frame, columns=cart_cols, show='headings', height=8)

        self.cart_tree.heading('Product ID', text='#')
        self.cart_tree.column('Product ID', width=40, anchor='center')

        self.cart_tree.heading('Product Name', text='Product')
        self.cart_tree.column('Product Name', width=180, anchor='w')

        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.column('Price', width=80, anchor='center')

        self.cart_tree.heading('Qty', text='Qty')
        self.cart_tree.column('Qty', width=50, anchor='center')

        self.cart_tree.heading('Subtotal', text='Subtotal')
        self.cart_tree.column('Subtotal', width=100, anchor='e')

        cart_vscroll = ttk.Scrollbar(cart_tree_frame, orient='vertical', command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=cart_vscroll.set)

        self.cart_tree.grid(row=0, column=0, sticky='nsew')
        cart_vscroll.grid(row=0, column=1, sticky='ns')

        cart_tree_frame.grid_rowconfigure(0, weight=1)
        cart_tree_frame.grid_columnconfigure(0, weight=1)

        # Remove item button
        remove_btn = tk.Button(cart_frame, text="🗑️ Remove Selected Item", command=self.remove_from_cart,
                               bg='#c0392b', fg='white', font=('Arial', 10, 'bold'),
                               relief='flat', padx=10, pady=5)
        remove_btn.pack(pady=5)

        # Summary section - MADE MORE COMPACT
        summary_frame = tk.Frame(cart_frame, bg='#ecf0f1', relief='solid', bd=1)
        summary_frame.pack(fill='x', padx=10, pady=5)

        subtotal_container = tk.Frame(summary_frame, bg='#ecf0f1')
        subtotal_container.pack(fill='x', padx=10, pady=3)
        tk.Label(subtotal_container, text="Subtotal:", font=('Arial', 10), bg='#ecf0f1').pack(side='left')
        self.subtotal_label = tk.Label(subtotal_container, text="₱0.00", font=('Arial', 10, 'bold'),
                                       bg='#ecf0f1', fg='#2c3e50')
        self.subtotal_label.pack(side='right')

        disc_container = tk.Frame(summary_frame, bg='#ecf0f1')
        disc_container.pack(fill='x', padx=10, pady=3)
        tk.Label(disc_container, text="Discount (%):", font=('Arial', 9), bg='#ecf0f1').pack(side='left')
        self.disc_entry = tk.Entry(disc_container, width=8, font=('Arial', 9))
        self.disc_entry.pack(side='right', padx=5)
        apply_disc_btn = tk.Button(disc_container, text="Apply", command=self.apply_discount,
                                   bg='#f39c12', fg='white', font=('Arial', 8, 'bold'), relief='flat', padx=8)
        apply_disc_btn.pack(side='right')

        total_container = tk.Frame(summary_frame, bg='#2c3e50', pady=8)
        total_container.pack(fill='x', pady=(5, 0))
        tk.Label(total_container, text="TOTAL:", font=('Arial', 12, 'bold'),
                 bg='#2c3e50', fg='white').pack(side='left', padx=10)
        self.total_label = tk.Label(total_container, text="₱0.00", font=('Arial', 14, 'bold'),
                                    bg='#2c3e50', fg='#2ecc71')
        self.total_label.pack(side='right', padx=10)

        # Payment section - MADE MORE COMPACT
        payment_frame = tk.Frame(cart_frame, bg='white')
        payment_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(payment_frame, text="Payment Method:", bg='white',
                 font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', pady=3)

        self.payment_var = tk.StringVar(value='cash')
        payment_btns = tk.Frame(payment_frame, bg='white')
        payment_btns.grid(row=0, column=1, sticky='w', padx=10)

        rb_cash = tk.Radiobutton(payment_btns, text="Cash", variable=self.payment_var, value="cash",
                                 bg='white', font=('Arial', 9))
        rb_cash.pack(side='left', padx=5)
        rb_card = tk.Radiobutton(payment_btns, text="Card", variable=self.payment_var, value="card",
                                 bg='white', font=('Arial', 9))
        rb_card.pack(side='left', padx=5)

        tk.Label(payment_frame, text="Amount Tendered:", bg='white',
                 font=('Arial', 9)).grid(row=1, column=0, sticky='w', pady=3)
        self.amount_entry = tk.Entry(payment_frame, width=15, font=('Arial', 10))
        self.amount_entry.grid(row=1, column=1, sticky='w', padx=10)
        self.amount_entry.bind("<KeyRelease>", lambda e: self.calculate_change())

        self.change_label = tk.Label(payment_frame, text="Change: ₱0.00", font=('Arial', 10, 'bold'),
                                     bg='white', fg='#27ae60')
        self.change_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=5)

        # Action buttons - BIGGER AND MORE VISIBLE
        action_frame = tk.Frame(cart_frame, bg='white')
        action_frame.pack(fill='x', padx=10, pady=5)

        complete_btn = tk.Button(action_frame, text="✓ COMPLETE SALE", command=self.checkout,
                                 bg='#27ae60', fg='white', font=('Arial', 13, 'bold'),
                                 relief='flat', pady=15, cursor='hand2')
        complete_btn.pack(fill='x', pady=2)

        self.print_receipt_btn = tk.Button(
            action_frame,
            text="🖨 Print Receipt",
            command=self.print_last_receipt,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            pady=10,
            cursor='hand2',
            state="disabled"
        )
        self.print_receipt_btn.pack(fill='x', pady=2)

        cancel_btn = tk.Button(action_frame, text="✗ Cancel Sale", command=self.cancel_sale,
                               bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                               relief='flat', pady=10, cursor='hand2')
        cancel_btn.pack(fill='x', pady=2)

        self.update_cart_display()

    def load_products(self, search_term=''):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        query = "SELECT id, name, price, stock FROM products WHERE name LIKE %s OR category LIKE %s ORDER BY name"
        results = self.db.execute_query(query, (f'%{search_term}%', f'%{search_term}%'), fetch=True)

        if results:
            for seq, row in enumerate(results, start=1):
                db_id, name, price, stock = row
                price_str = f"₱{float(price):.2f}"
                stock_str = f"{int(float(stock))}" if float(stock).is_integer() else f"{float(stock):.1f}"
                self.product_tree.insert('', 'end', iid=str(db_id), values=(seq, name, price_str, stock_str))

    def search_products(self):
        search_term = self.search_entry.get()
        self.load_products(search_term)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_products()

    def on_product_select_tree(self, event):
        pass

    def add_to_cart(self):
        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a product from the list first.")
            return

        product_id = int(selection[0])
        item_values = self.product_tree.item(selection[0], 'values')
        name = item_values[1]
        price_str = item_values[2].replace('₱', '')
        price = float(price_str)

        try:
            stock_str = item_values[3]
            available_stock = float(stock_str)
        except ValueError:
            messagebox.showerror("Error", "Product stock data is corrupted.")
            return

        try:
            qty_input = self.qty_entry.get()
            if not qty_input:
                messagebox.showerror("Error", "Quantity cannot be empty.")
                return
            qty = int(qty_input)
            if qty <= 0:
                raise ValueError("Quantity must be positive.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid whole number quantity.")
            return

        existing_item_index = -1
        for i, item in enumerate(self.cart):
            if item['product_id'] == product_id:
                existing_item_index = i
                break

        if existing_item_index != -1:
            new_total_qty = self.cart[existing_item_index]['qty'] + qty
            if available_stock < new_total_qty:
                messagebox.showerror("Error",
                                     f"Insufficient stock for {name}.\nAvailable: {available_stock}\nIn cart: {self.cart[existing_item_index]['qty']}")
                return
            self.cart[existing_item_index]['qty'] = new_total_qty
            self.cart[existing_item_index]['subtotal'] = new_total_qty * price
        else:
            if available_stock < qty:
                messagebox.showerror("Error", f"Insufficient stock for {name}.\nAvailable: {available_stock}")
                return
            subtotal = price * qty
            self.cart.append({'product_id': product_id, 'name': name, 'price': price, 'qty': qty, 'subtotal': subtotal})

        self.update_cart_display()
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")

    def remove_from_cart(self):
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select an item to remove from cart.")
            return

        item_values = self.cart_tree.item(selection[0], 'values')
        sequence_num = int(item_values[0])

        if 0 < sequence_num <= len(self.cart):
            self.cart.pop(sequence_num - 1)

        self.update_cart_display()

    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        subtotal_val = 0.0
        for idx, item in enumerate(self.cart, start=1):
            self.cart_tree.insert('', 'end',
                                  values=(idx, item['name'],
                                          f"₱{item['price']:.2f}", int(item['qty']),
                                          f"₱{item['subtotal']:.2f}"))
            subtotal_val += item['subtotal']

        self.subtotal_label.config(text=f"₱{subtotal_val:.2f}")

        try:
            disc_pct = float(self.disc_entry.get() or 0) / 100
            if not (0 <= disc_pct <= 1):
                raise ValueError
            self.discount = subtotal_val * disc_pct
        except ValueError:
            self.discount = 0.0

        final_total = subtotal_val - self.discount
        self.total_label.config(text=f"₱{final_total:.2f}")
        self.calculate_change()

    def apply_discount(self):
        self.update_cart_display()

    def _show_invalid_amount_panel(self):
        panel = tk.Toplevel(self.root)
        panel.title("Invalid Input")
        panel.geometry("320x120")
        panel.transient(self.root)
        panel.grab_set()
        panel.resizable(False, False)

        tk.Label(panel, text="Please input a correct number.", font=('Arial', 11), pady=10).pack()
        tk.Label(panel, text="Amount tendered cannot be negative.", font=('Arial', 9), fg='#c0392b').pack()

        def close_panel():
            panel.destroy()
            self.amount_entry.focus_set()

        ok_btn = tk.Button(panel, text="OK", command=close_panel, bg='#3498db', fg='white', padx=12, pady=6)
        ok_btn.pack(pady=10)

    def calculate_change(self):
        final_total_str = self.total_label.cget("text").replace("₱", "")
        final_total = float(final_total_str)

        amount_input = self.amount_entry.get().strip()

        if not amount_input:
            self.change_label.config(text="Change: ₱0.00", fg="#27ae60")
            return

        try:
            amount_tendered = float(amount_input)

            if amount_tendered < 0:
                self._show_invalid_amount_panel()
                return

            change = amount_tendered - final_total

            if change < 0:
                self.change_label.config(text="Insufficient payment", fg="#e74c3c")
                return

            self.change_label.config(text=f"Change: ₱{change:.2f}", fg="#27ae60")

        except ValueError:
            self.change_label.config(text="Invalid input", fg="#e74c3c")

    def checkout(self):
        """Process the sale and complete checkout"""
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty. Please add items before checkout.")
            return

        payment_method = self.payment_var.get()
        final_total_str = self.total_label.cget("text").replace("₱", "").replace(",", "")
        final_total = float(final_total_str)

        amount_tendered = final_total
        change = 0.0

        if payment_method == 'cash':
            amount_input = self.amount_entry.get().strip()

            if not amount_input:
                messagebox.showerror("Error", "Please enter amount tendered for cash payment.")
                self.amount_entry.focus()
                return

            try:
                amount_tendered = float(amount_input)

                if amount_tendered < 0:
                    messagebox.showerror("Error", "Amount tendered cannot be negative.")
                    return

                if amount_tendered < final_total:
                    messagebox.showerror("Error",
                                         f"Insufficient payment.\nTotal: ₱{final_total:.2f}\nTendered: ₱{amount_tendered:.2f}")
                    return

                change = amount_tendered - final_total
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
                self.amount_entry.focus()
                return

        # Start database transaction
        try:
            # Save sale to database
            sale_query = "INSERT INTO sales (cashier_id, total, discount, payment_method) VALUES (%s, %s, %s, %s)"
            sale_result = self.db.execute_query(sale_query,
                                                (self.cashier_id, final_total, self.discount, payment_method),
                                                fetch=False)

            if not sale_result:
                messagebox.showerror("Error", "Failed to record sale in database.")
                return

            # Get the sale ID
            sale_id = self.db.cursor.lastrowid

            # Insert sale items and update stock
            for item in self.cart:
                # Insert sale item
                item_query = "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
                self.db.execute_query(item_query, (sale_id, item['product_id'], item['qty'], item['price']))

                # Update product stock
                stock_query = "UPDATE products SET stock = stock - %s WHERE id = %s"
                self.db.execute_query(stock_query, (item['qty'], item['product_id']))

            # Reload products to show updated stock
            self.load_products()

            # Log activity
            log_query = "INSERT INTO cashier_logs (cashier_id, activity) VALUES (%s, 'Transaction completed')"
            self.db.execute_query(log_query, (self.cashier_id,))

            # Store sale info for print receipt
            self.last_sale_id = sale_id
            self.last_payment_method = payment_method
            self.last_final_total = final_total
            self.last_amount_tendered = amount_tendered
            self.last_change = change
            self.last_cart_items = self.cart.copy()

            # Print Receipt automatically
            self.print_receipt(sale_id, payment_method, final_total, amount_tendered, change)

            # Reset the sale
            self.reset_sale()

            # Enable print receipt button
            self.print_receipt_btn.config(state="normal")

            # Show success message
            messagebox.showinfo("Success",
                                f"Transaction completed successfully!\n\nReceipt #: {sale_id}\nTotal: ₱{final_total:,.2f}\nChange: ₱{change:,.2f}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during checkout:\n{str(e)}")
            print(f"Checkout error: {str(e)}")
            import traceback
            traceback.print_exc()

    def cancel_sale(self):
        if not self.cart:
            messagebox.showinfo("Info", "Cart is already empty.")
            return

        if messagebox.askyesno("Confirm Cancel",
                               "Are you sure you want to cancel this sale?\nAll items will be removed from the cart."):
            # Log the cancellation
            log_query = "INSERT INTO cashier_logs (cashier_id, activity) VALUES (%s, 'Sale cancelled')"
            self.db.execute_query(log_query, (self.cashier_id,))

            self.reset_sale()
            messagebox.showinfo("Sale Cancelled", "The current sale has been cancelled and the cart cleared.")

    def reset_sale(self):
        self.cart = []
        self.discount = 0.0
        try:
            self.disc_entry.delete(0, tk.END)
        except Exception:
            pass
        try:
            self.amount_entry.delete(0, tk.END)
        except Exception:
            pass
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self.update_cart_display()
        self.change_label.config(text="Change: ₱0.00", fg="#27ae60")

    def print_receipt(self, sale_id, payment_method, final_total, amount_tendered, change):
        """Print receipt for a completed sale"""
        receipt_win = tk.Toplevel(self.root)
        receipt_win.title("Receipt")
        receipt_win.geometry("420x560")
        receipt_win.configure(bg="white")
        receipt_win.resizable(False, False)
        receipt_win.transient(self.root)

        receipt_win.update_idletasks()
        width = receipt_win.winfo_width()
        height = receipt_win.winfo_height()
        x = (receipt_win.winfo_screenwidth() // 2) - (width // 2)
        y = (receipt_win.winfo_screenheight() // 2) - (height // 2)
        receipt_win.geometry(f'{width}x{height}+{x}+{y}')

        WIDTH = 48
        NAME_W = 22
        QTY_W = 5
        PRICE_W = 11
        SUB_W = 10

        lines = []
        lines.append("NABUNTURAN GROCERY STORE".center(WIDTH))
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(WIDTH))
        lines.append(f"Receipt #: {sale_id}".center(WIDTH))
        lines.append("-" * WIDTH)
        header = f"{'Item':<{NAME_W}}{'Qty':>{QTY_W}}{'Price':>{PRICE_W}}{'Subtotal':>{SUB_W}}"
        lines.append(header)
        lines.append("-" * WIDTH)

        subtotal_sum = 0.0
        for item in self.last_cart_items:
            name = item['name'][:NAME_W]
            qty = int(item['qty'])
            price = float(item.get('price', 0.0))
            subtotal = float(item.get('subtotal', 0.0))
            subtotal_sum += subtotal
            price_str = f"₱{price:,.2f}"
            sub_str = f"₱{subtotal:,.2f}"
            line = f"{name:<{NAME_W}}{qty:>{QTY_W}}{price_str:>{PRICE_W}}{sub_str:>{SUB_W}}"
            lines.append(line)

        lines.append("-" * WIDTH)
        lines.append(f"{'Subtotal:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{subtotal_sum:,.2f}':>{SUB_W}}")
        if self.discount and self.discount > 0:
            lines.append(f"{'Discount:':<{NAME_W + QTY_W + PRICE_W}}{f'-₱{self.discount:,.2f}':>{SUB_W}}")
        lines.append(f"{'TOTAL:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{final_total:,.2f}':>{SUB_W}}")
        lines.append(f"{'Payment Method:':<{NAME_W + QTY_W + PRICE_W}}{payment_method.upper():>{SUB_W}}")
        lines.append(f"{'Amount Tendered:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{amount_tendered:,.2f}':>{SUB_W}}")
        lines.append(f"{'Change:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{change:,.2f}':>{SUB_W}}")
        lines.append("-" * WIDTH)
        lines.append("Thank you for shopping with us!".center(WIDTH))
        receipt_text = "\n".join(lines)

        text_widget = scrolledtext.ScrolledText(
            receipt_win, wrap=tk.NONE,
            font=('Courier New', 10),
            bg='white', relief='flat', borderwidth=0
        )
        text_widget.insert(tk.END, receipt_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(receipt_win, bg="white")
        btn_frame.pack(pady=10)

        close_btn = tk.Button(
            btn_frame, text="Close",
            bg="#3498db", fg="white",
            font=("Arial", 10, "bold"),
            relief="flat", padx=20, pady=6,
            command=receipt_win.destroy
        )
        close_btn.pack(side="left", padx=10)

    def print_last_receipt(self):
        """Print the last completed sale receipt or current cart preview"""
        if hasattr(self, 'last_sale_id') and self.last_sale_id is not None:
            self.print_receipt(
                self.last_sale_id,
                self.last_payment_method,
                self.last_final_total,
                self.last_amount_tendered,
                self.last_change
            )
        elif self.cart:
            self.print_cart_preview()
        else:
            messagebox.showwarning("No Receipt",
                                   "No transaction to print.\nAdd items to cart or complete a sale first.")

    def print_cart_preview(self):
        """Print a preview of the current cart (not yet completed)"""
        final_total_str = self.total_label.cget("text").replace("₱", "")
        final_total = float(final_total_str)

        amount_input = self.amount_entry.get().strip()
        if amount_input:
            try:
                amount_tendered = float(amount_input)
                change = amount_tendered - final_total
            except ValueError:
                amount_tendered = 0.0
                change = 0.0
        else:
            amount_tendered = 0.0
            change = 0.0

        payment_method = self.payment_var.get()

        receipt_win = tk.Toplevel(self.root)
        receipt_win.title("Cart Preview")
        receipt_win.geometry("420x560")
        receipt_win.configure(bg="white")
        receipt_win.resizable(False, False)
        receipt_win.transient(self.root)

        WIDTH = 48
        NAME_W = 22
        QTY_W = 5
        PRICE_W = 11
        SUB_W = 10

        lines = []
        lines.append("NABUNTURAN GROCERY STORE".center(WIDTH))
        lines.append("*** CART PREVIEW - NOT FINAL ***".center(WIDTH))
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(WIDTH))
        lines.append("-" * WIDTH)
        header = f"{'Item':<{NAME_W}}{'Qty':>{QTY_W}}{'Price':>{PRICE_W}}{'Subtotal':>{SUB_W}}"
        lines.append(header)
        lines.append("-" * WIDTH)

        subtotal_sum = 0.0
        for item in self.cart:
            name = item['name'][:NAME_W]
            qty = int(item['qty'])
            price = float(item.get('price', 0.0))
            subtotal = float(item.get('subtotal', 0.0))
            subtotal_sum += subtotal
            price_str = f"₱{price:,.2f}"
            sub_str = f"₱{subtotal:,.2f}"
            line = f"{name:<{NAME_W}}{qty:>{QTY_W}}{price_str:>{PRICE_W}}{sub_str:>{SUB_W}}"
            lines.append(line)

        lines.append("-" * WIDTH)
        lines.append(f"{'Subtotal:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{subtotal_sum:,.2f}':>{SUB_W}}")
        if self.discount and self.discount > 0:
            lines.append(f"{'Discount:':<{NAME_W + QTY_W + PRICE_W}}{f'-₱{self.discount:,.2f}':>{SUB_W}}")
        lines.append(f"{'TOTAL:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{final_total:,.2f}':>{SUB_W}}")
        lines.append(f"{'Payment Method:':<{NAME_W + QTY_W + PRICE_W}}{payment_method.upper():>{SUB_W}}")
        if amount_tendered > 0:
            lines.append(f"{'Amount Tendered:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{amount_tendered:,.2f}':>{SUB_W}}")
            lines.append(f"{'Change:':<{NAME_W + QTY_W + PRICE_W}}{f'₱{change:,.2f}':>{SUB_W}}")
        lines.append("-" * WIDTH)
        lines.append("*** PREVIEW ONLY ***".center(WIDTH))
        lines.append("Click 'Complete Sale' to finalize".center(WIDTH))
        receipt_text = "\n".join(lines)

        text_widget = scrolledtext.ScrolledText(
            receipt_win, wrap=tk.NONE,
            font=('Courier New', 10),
            bg='white', relief='flat', borderwidth=0
        )
        text_widget.insert(tk.END, receipt_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(receipt_win, bg="white")
        btn_frame.pack(pady=10)

        close_btn = tk.Button(
            btn_frame, text="Close",
            bg="#3498db", fg="white",
            font=("Arial", 10, "bold"),
            relief="flat", padx=20, pady=6,
            command=receipt_win.destroy
        )
        close_btn.pack(side="left", padx=10)

    def logout(self):
        from login_window import LoginWindow

        log_query = "INSERT INTO cashier_logs (cashier_id, activity) VALUES (%s, 'Time-out')"
        self.db.execute_query(log_query, (self.cashier_id,))
        self.db.close()
        self.root.destroy()

        login_root = tk.Tk()
        LoginWindow(login_root)
        login_root.mainloop()