import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
from database import Database


class AdminWindow:
    def __init__(self, root, admin_name, logout_callback):
        self.root = root
        self.root.title(f"Nabunturan POS - Admin: {admin_name}")
        self.root.geometry("1200x750")
        self.root.state('zoomed')

        self.db = Database()
        self.admin_name = admin_name
        self.logout_callback = logout_callback

        # Fonts
        self.title_font = font.Font(family="Arial", size=18, weight="bold")
        self.header_font = font.Font(family="Arial", size=13, weight="bold")
        self.normal_font = font.Font(family="Arial", size=10)

        # Styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#e0e0e0')
        self.style.configure('TLabel', background='#e0e0e0')
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        self.style.configure('Treeview', rowheight=25, font=('Arial', 10))
        self.style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))

        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

        # Left Navigation Panel
        nav_frame = tk.Frame(main_frame, width=220, bg='#2c3e50')
        nav_frame.pack(side='left', fill='y', padx=(0, 10))
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text="ADMIN PANEL", font=('Arial', 14, 'bold'),
                 bg='#2c3e50', fg='white').pack(pady=(20, 5))
        tk.Label(nav_frame, text=admin_name, font=('Arial', 10),
                 bg='#2c3e50', fg='white').pack(pady=(0, 20))

        # Navigation buttons
        self.btn_dashboard = tk.Button(nav_frame, text="Dashboard",
                                       command=lambda: self.show_dashboard(),
                                       bg='#1abc9c', fg='white', font=('Arial', 10, 'bold'),
                                       relief='flat', padx=10, pady=10)
        self.btn_dashboard.pack(fill='x', pady=5, padx=10)

        self.btn_products = tk.Button(nav_frame, text="Products",
                                      command=lambda: self.show_products(),
                                      bg='#34495e', fg='white', font=('Arial', 10, 'bold'),
                                      relief='flat', padx=10, pady=10)
        self.btn_products.pack(fill='x', pady=5, padx=10)

        self.btn_sales = tk.Button(nav_frame, text="Sales",
                                   command=lambda: self.show_sales(),
                                   bg='#34495e', fg='white', font=('Arial', 10, 'bold'),
                                   relief='flat', padx=10, pady=10)
        self.btn_sales.pack(fill='x', pady=5, padx=10)

        self.btn_cashiers = tk.Button(nav_frame, text="Cashiers",
                                      command=lambda: self.show_cashiers(),
                                      bg='#34495e', fg='white', font=('Arial', 10, 'bold'),
                                      relief='flat', padx=10, pady=10)
        self.btn_cashiers.pack(fill='x', pady=5, padx=10)

        self.btn_reports = tk.Button(nav_frame, text="Reports",
                                     command=lambda: self.show_reports(),
                                     bg='#34495e', fg='white', font=('Arial', 10, 'bold'),
                                     relief='flat', padx=10, pady=10)
        self.btn_reports.pack(fill='x', pady=5, padx=10)

        # Logout button
        logout_btn = tk.Button(nav_frame, text="Logout", command=self.logout,
                               bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                               relief='flat', padx=10, pady=10)
        logout_btn.pack(fill='x', pady=(50, 10), padx=10, side='bottom')

        # Right Content Area
        self.content_frame = tk.Frame(main_frame, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Status bar
        self.status_frame = tk.Frame(main_frame, bg='#34495e', height=30)
        self.status_frame.pack(side='bottom', fill='x')

        self.status_label = tk.Label(self.status_frame, text="Ready",
                                     bg='#34495e', fg='white', font=('Arial', 9))
        self.status_label.pack(side='left', padx=10, pady=5)

        # Show dashboard by default
        self.show_dashboard()

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_status(self, message, color="#34495e"):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.status_frame.config(bg=color)
        self.status_label.config(bg=color)
        self.root.after(3000, lambda: self.reset_status())

    def reset_status(self):
        """Reset status bar to default"""
        self.status_label.config(text="Ready")
        self.status_frame.config(bg="#34495e")
        self.status_label.config(bg="#34495e")

    def highlight_nav_button(self, active_button):
        """Highlight the active navigation button"""
        buttons = [self.btn_dashboard, self.btn_products, self.btn_sales,
                   self.btn_cashiers, self.btn_reports]
        for btn in buttons:
            btn.config(bg='#34495e')
        active_button.config(bg='#1abc9c')

    def show_dashboard(self):
        """Display admin dashboard"""
        self.clear_content()
        self.highlight_nav_button(self.btn_dashboard)

        # Title
        title_frame = tk.Frame(self.content_frame, bg='white', padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        tk.Label(title_frame, text="Dashboard", font=self.title_font,
                 bg='white', fg='#2c3e50').pack(side=tk.LEFT)

        tk.Label(title_frame, text=f"Welcome, {self.admin_name}",
                 font=self.normal_font, bg='white', fg='#7f8c8d').pack(side=tk.RIGHT)

        # Statistics cards
        stats_frame = tk.Frame(self.content_frame, bg='white', padx=20)
        stats_frame.pack(fill=tk.X, pady=20)

        # Get statistics
        stats = self.get_dashboard_stats()

        cards = [
            ("Total Products", str(stats['total_products']), "#3498db", "📦"),
            ("Today's Sales", f"₱{stats['today_sales']:,.2f}", "#2ecc71", "💰"),
            ("Active Cashiers", str(stats['total_cashiers']), "#9b59b6", "👥"),
            ("Low Stock Items", str(stats['low_stock']), "#e74c3c", "⚠️"),
        ]

        for i, (title, value, color, icon) in enumerate(cards):
            card = self.create_stat_card(stats_frame, title, value, color, icon)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")

        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

        # Recent activity section
        activity_frame = tk.Frame(self.content_frame, bg='white', relief='ridge', bd=1)
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        tk.Label(activity_frame, text="Recent Sales", font=self.header_font,
                 bg='white', fg='#2c3e50').pack(anchor='w', padx=20, pady=(20, 10))

        # Recent sales table
        columns = ("id", "cashier", "total", "time")
        tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=10)

        tree.heading("id", text="Receipt #")
        tree.heading("cashier", text="Cashier")
        tree.heading("total", text="Total")
        tree.heading("time", text="Time")

        tree.column("id", width=100, anchor="center")
        tree.column("cashier", width=200, anchor="w")
        tree.column("total", width=150, anchor="e")
        tree.column("time", width=200, anchor="center")

        # Load recent sales
        recent_sales = self.get_recent_sales()
        for sale in recent_sales:
            tree.insert("", tk.END, values=sale)

        scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=(0, 20))

    def create_stat_card(self, parent, title, value, color, icon):
        """Create a statistics card"""
        card = tk.Frame(parent, bg="white", relief=tk.SOLID, bd=1, padx=20, pady=20)

        icon_label = tk.Label(card, text=icon, font=("Arial", 32), bg="white")
        icon_label.pack()

        value_label = tk.Label(card, text=value, font=("Arial", 24, "bold"),
                               bg="white", fg=color)
        value_label.pack(pady=(10, 5))

        title_label = tk.Label(card, text=title, font=self.normal_font,
                               bg="white", fg="#7f8c8d")
        title_label.pack()

        return card

    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        # Total products
        products_query = "SELECT COUNT(*) FROM products"
        products_result = self.db.execute_query(products_query, fetch=True)
        total_products = products_result[0][0] if products_result else 0

        # Today's sales
        sales_query = """
            SELECT COALESCE(SUM(total), 0) 
            FROM sales 
            WHERE DATE(date) = CURDATE() AND payment_method != 'report'
        """
        sales_result = self.db.execute_query(sales_query, fetch=True)
        today_sales = float(sales_result[0][0]) if sales_result else 0.0

        # Total cashiers
        cashiers_query = "SELECT COUNT(*) FROM cashiers"
        cashiers_result = self.db.execute_query(cashiers_query, fetch=True)
        total_cashiers = cashiers_result[0][0] if cashiers_result else 0

        # Low stock items (stock < 10)
        low_stock_query = "SELECT COUNT(*) FROM products WHERE stock < 10"
        low_stock_result = self.db.execute_query(low_stock_query, fetch=True)
        low_stock = low_stock_result[0][0] if low_stock_result else 0

        return {
            'total_products': total_products,
            'today_sales': today_sales,
            'total_cashiers': total_cashiers,
            'low_stock': low_stock
        }

    def get_recent_sales(self):
        """Get recent sales"""
        query = """
            SELECT s.id, c.name, s.total, TIME_FORMAT(s.date, '%h:%i %p')
            FROM sales s
            JOIN cashiers c ON s.cashier_id = c.id
            WHERE DATE(s.date) = CURDATE() AND s.payment_method != 'report'
            ORDER BY s.date DESC
            LIMIT 10
        """
        results = self.db.execute_query(query, fetch=True)

        if results:
            return [(row[0], row[1], f"₱{float(row[2]):,.2f}", row[3]) for row in results]
        return []

    def show_products(self):
        """Display products management interface"""
        self.clear_content()
        self.highlight_nav_button(self.btn_products)
        self.current_view = tk.StringVar(value='products')

        # Title section
        title_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        title = tk.Label(title_frame, text="Products Management", font=self.title_font, bg="white", fg="#2c3e50")
        title.pack(side=tk.LEFT)

        # Action buttons
        btn_frame = tk.Frame(title_frame, bg="white")
        btn_frame.pack(side=tk.RIGHT)

        add_btn = tk.Button(btn_frame, text="+ Add Product", command=self.add_product,
                            bg="#27ae60", fg="white", font=self.normal_font,
                            relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.show_products,
                                bg="#3498db", fg="white", font=self.normal_font,
                                relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Search section
        search_frame = tk.Frame(self.content_frame, bg="#ecf0f1", padx=20, pady=15)
        search_frame.pack(fill=tk.X)

        search_label = tk.Label(search_frame, text="Search:", bg="#ecf0f1", font=self.normal_font)
        search_label.pack(side=tk.LEFT, padx=(0, 10))

        self.product_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.product_search_var,
                                width=40, font=self.normal_font)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.load_products())

        # Products table
        table_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "category", "price", "stock")
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.products_tree.heading("id", text="ID")
        self.products_tree.heading("name", text="Product Name")
        self.products_tree.heading("category", text="Category")
        self.products_tree.heading("price", text="Price")
        self.products_tree.heading("stock", text="Stock")

        self.products_tree.column("id", width=60, anchor="center")
        self.products_tree.column("name", width=300, anchor="w")
        self.products_tree.column("category", width=150, anchor="w")
        self.products_tree.column("price", width=120, anchor="e")
        self.products_tree.column("stock", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)

        action_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=(0, 20))
        action_frame.pack(fill=tk.X)

        edit_btn = tk.Button(action_frame, text="Edit Selected", command=self.edit_product,
                             bg="#f39c12", fg="white", font=self.normal_font,
                             relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(action_frame, text="Delete Selected", command=self.delete_product,
                               bg="#e74c3c", fg="white", font=self.normal_font,
                               relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        delete_btn.pack(side=tk.LEFT, padx=5)

        self.load_products()

    def load_products(self):
        """Load products from database"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)

        search_term = self.product_search_var.get() if hasattr(self, 'product_search_var') else ''

        query = "SELECT id, name, category, price, stock FROM products WHERE name LIKE %s OR category LIKE %s ORDER BY name"
        results = self.db.execute_query(query, (f'%{search_term}%', f'%{search_term}%'), fetch=True)

        if results:
            for row in results:
                product_id, name, category, price, stock = row
                self.products_tree.insert('', 'end', values=(
                    product_id,
                    name,
                    category,
                    f"₱{float(price):,.2f}",
                    int(stock) if float(stock).is_integer() else f"{float(stock):.1f}"
                ))

    def add_product(self):
        """Show add product dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("450x400")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

        title = tk.Label(dialog, text="Add New Product", font=self.header_font, bg="white", fg="#2c3e50")
        title.pack(pady=20)

        form_frame = tk.Frame(dialog, bg="white", padx=30)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Product Name:", bg="white", font=self.normal_font).grid(row=0, column=0, sticky="w",
                                                                                           pady=10)
        name_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        name_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Category:", bg="white", font=self.normal_font).grid(row=1, column=0, sticky="w",
                                                                                       pady=10)
        category_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        category_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Price:", bg="white", font=self.normal_font).grid(row=2, column=0, sticky="w",
                                                                                    pady=10)
        price_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        price_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Stock:", bg="white", font=self.normal_font).grid(row=3, column=0, sticky="w",
                                                                                    pady=10)
        stock_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        stock_entry.grid(row=3, column=1, pady=10, padx=10)

        def save_product():
            name = name_entry.get().strip()
            category = category_entry.get().strip()
            price = price_entry.get().strip()
            stock = stock_entry.get().strip()

            if not all([name, category, price, stock]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                price = float(price)
                stock = float(stock)
                if price <= 0 or stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid price or stock value!")
                return

            query = "INSERT INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)"
            if self.db.execute_query(query, (name, category, price, stock)):
                messagebox.showinfo("Success", "Product added successfully!")
                dialog.destroy()
                self.load_products()
                self.update_status("Product added successfully", "#27ae60")
            else:
                messagebox.showerror("Error", "Failed to add product!")

        btn_frame = tk.Frame(dialog, bg="white", pady=20)
        btn_frame.pack()

        save_btn = tk.Button(btn_frame, text="Save", command=save_product,
                             bg="#27ae60", fg="white", font=self.normal_font,
                             relief=tk.FLAT, padx=30, pady=10, cursor="hand2")
        save_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                               bg="#95a5a6", fg="white", font=self.normal_font,
                               relief=tk.FLAT, padx=30, pady=10, cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def edit_product(self):
        """Edit selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to edit!")
            return

        item = self.products_tree.item(selection[0])
        values = item['values']
        product_id = values[0]

        query = "SELECT name, category, price, stock FROM products WHERE id = %s"
        result = self.db.execute_query(query, (product_id,), fetch=True)

        if not result:
            messagebox.showerror("Error", "Product not found!")
            return

        name, category, price, stock = result[0]

        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("450x400")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

        title = tk.Label(dialog, text=f"Edit Product #{product_id}", font=self.header_font, bg="white", fg="#2c3e50")
        title.pack(pady=20)

        form_frame = tk.Frame(dialog, bg="white", padx=30)
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Product Name:", bg="white", font=self.normal_font).grid(row=0, column=0, sticky="w",
                                                                                           pady=10)
        name_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Category:", bg="white", font=self.normal_font).grid(row=1, column=0, sticky="w",
                                                                                       pady=10)
        category_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        category_entry.insert(0, category)
        category_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Price:", bg="white", font=self.normal_font).grid(row=2, column=0, sticky="w",
                                                                                    pady=10)
        price_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        price_entry.insert(0, str(price))
        price_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Stock:", bg="white", font=self.normal_font).grid(row=3, column=0, sticky="w",
                                                                                    pady=10)
        stock_entry = tk.Entry(form_frame, width=30, font=self.normal_font)
        stock_entry.insert(0, str(stock))
        stock_entry.grid(row=3, column=1, pady=10, padx=10)

        def update_product():
            new_name = name_entry.get().strip()
            new_category = category_entry.get().strip()
            new_price = price_entry.get().strip()
            new_stock = stock_entry.get().strip()

            if not all([new_name, new_category, new_price, new_stock]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                new_price = float(new_price)
                new_stock = float(new_stock)
                if new_price <= 0 or new_stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid price or stock value!")
                return

            query = "UPDATE products SET name=%s, category=%s, price=%s, stock=%s WHERE id=%s"
            if self.db.execute_query(query, (new_name, new_category, new_price, new_stock, product_id)):
                messagebox.showinfo("Success", "Product updated successfully!")
                dialog.destroy()
                self.load_products()
                self.update_status("Product updated successfully", "#27ae60")
            else:
                messagebox.showerror("Error", "Failed to update product!")

        btn_frame = tk.Frame(dialog, bg="white", pady=20)
        btn_frame.pack()

        update_btn = tk.Button(btn_frame, text="Update", command=update_product,
                               bg="#f39c12", fg="white", font=self.normal_font,
                               relief=tk.FLAT, padx=30, pady=10, cursor="hand2")
        update_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                               bg="#95a5a6", fg="white", font=self.normal_font,
                               relief=tk.FLAT, padx=30, pady=10, cursor="hand2")
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def delete_product(self):
        """Delete selected product"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to delete!")
            return

        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            query = "DELETE FROM products WHERE id = %s"
            if self.db.execute_query(query, (product_id,)):
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_products()
                self.update_status("Product deleted successfully", "#27ae60")
            else:
                messagebox.showerror("Error", "Failed to delete product!")

    def show_sales(self):
        """Display sales management interface"""
        self.clear_content()
        self.highlight_nav_button(self.btn_sales)
        self.current_view = tk.StringVar(value='sales')

        title_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        title = tk.Label(title_frame, text="Sales Records", font=self.title_font, bg="white", fg="#2c3e50")
        title.pack(side=tk.LEFT)

        refresh_btn = tk.Button(title_frame, text="Refresh", command=self.show_sales,
                                bg="#3498db", fg="white", font=self.normal_font,
                                relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        refresh_btn.pack(side=tk.RIGHT)

        filter_frame = tk.Frame(self.content_frame, bg="#ecf0f1", padx=20, pady=15)
        filter_frame.pack(fill=tk.X)

        tk.Label(filter_frame, text="Filter by Date:", bg="#ecf0f1", font=self.normal_font).pack(side=tk.LEFT,
                                                                                                 padx=(0, 10))

        self.date_filter_var = tk.StringVar(value="today")

        tk.Radiobutton(filter_frame, text="Today", variable=self.date_filter_var, value="today",
                       bg="#ecf0f1", font=self.normal_font, command=self.load_sales).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(filter_frame, text="This Week", variable=self.date_filter_var, value="week",
                       bg="#ecf0f1", font=self.normal_font, command=self.load_sales).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(filter_frame, text="This Month", variable=self.date_filter_var, value="month",
                       bg="#ecf0f1", font=self.normal_font, command=self.load_sales).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(filter_frame, text="All", variable=self.date_filter_var, value="all",
                       bg="#ecf0f1", font=self.normal_font, command=self.load_sales).pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "cashier", "total", "discount", "payment", "date")
        self.sales_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.sales_tree.heading("id", text="Receipt #")
        self.sales_tree.heading("cashier", text="Cashier")
        self.sales_tree.heading("total", text="Total")
        self.sales_tree.heading("discount", text="Discount")
        self.sales_tree.heading("payment", text="Payment Method")
        self.sales_tree.heading("date", text="Date & Time")

        self.sales_tree.column("id", width=100, anchor="center")
        self.sales_tree.column("cashier", width=150, anchor="w")
        self.sales_tree.column("total", width=120, anchor="e")
        self.sales_tree.column("discount", width=100, anchor="e")
        self.sales_tree.column("payment", width=120, anchor="center")
        self.sales_tree.column("date", width=180, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_tree.pack(fill=tk.BOTH, expand=True)

        action_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=(0, 20))
        action_frame.pack(fill=tk.X)

        view_btn = tk.Button(action_frame, text="View Details", command=self.view_sale_details,
                             bg="#3498db", fg="white", font=self.normal_font,
                             relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        view_btn.pack(side=tk.LEFT, padx=5)

        self.load_sales()

    def load_sales(self):
        """Load sales from database based on filter"""
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        filter_type = self.date_filter_var.get()

        if filter_type == "today":
            query = """
                SELECT s.id, c.name, s.total, s.discount, s.payment_method, s.date
                FROM sales s
                JOIN cashiers c ON s.cashier_id = c.id
                WHERE DATE(s.date) = CURDATE() AND s.payment_method != 'report'
                ORDER BY s.date DESC
            """
        elif filter_type == "week":
            query = """
                SELECT s.id, c.name, s.total, s.discount, s.payment_method, s.date
                FROM sales s
                JOIN cashiers c ON s.cashier_id = c.id
                WHERE YEARWEEK(s.date) = YEARWEEK(NOW()) AND s.payment_method != 'report'
                ORDER BY s.date DESC
            """
        elif filter_type == "month":
            query = """
                SELECT s.id, c.name, s.total, s.discount, s.payment_method, s.date
                FROM sales s
                JOIN cashiers c ON s.cashier_id = c.id
                WHERE MONTH(s.date) = MONTH(NOW()) AND YEAR(s.date) = YEAR(NOW()) AND s.payment_method != 'report'
                ORDER BY s.date DESC
            """
        else:
            query = """
                SELECT s.id, c.name, s.total, s.discount, s.payment_method, s.date
                FROM sales s
                JOIN cashiers c ON s.cashier_id = c.id
                WHERE s.payment_method != 'report'
                ORDER BY s.date DESC
                LIMIT 1000
            """

        results = self.db.execute_query(query, fetch=True)

        if results:
            for row in results:
                sale_id, cashier, total, discount, payment, date = row
                self.sales_tree.insert('', 'end', values=(
                    sale_id,
                    cashier,
                    f"₱{float(total):,.2f}",
                    f"₱{float(discount):,.2f}",
                    payment.upper(),
                    date.strftime("%Y-%m-%d %I:%M %p")
                ))

    def view_sale_details(self):
        """View details of selected sale"""
        selection = self.sales_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a sale to view!")
            return

        item = self.sales_tree.item(selection[0])
        sale_id = item['values'][0]

        query = """
            SELECT p.name, si.quantity, si.price, (si.quantity * si.price) as subtotal
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
        """
        items = self.db.execute_query(query, (sale_id,), fetch=True)

        if not items:
            messagebox.showerror("Error", "Sale items not found!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Sale Details - Receipt #{sale_id}")
        dialog.geometry("500x600")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

        title = tk.Label(dialog, text=f"Receipt #{sale_id}", font=self.header_font, bg="white", fg="#2c3e50")
        title.pack(pady=20)

        columns = ("product", "qty", "price", "subtotal")
        tree = ttk.Treeview(dialog, columns=columns, show="headings", height=15)

        tree.heading("product", text="Product")
        tree.heading("qty", text="Qty")
        tree.heading("price", text="Price")
        tree.heading("subtotal", text="Subtotal")

        tree.column("product", width=200, anchor="w")
        tree.column("qty", width=60, anchor="center")
        tree.column("price", width=100, anchor="e")
        tree.column("subtotal", width=100, anchor="e")

        for item_row in items:
            product, qty, price, subtotal = item_row
            tree.insert('', 'end', values=(
                product,
                int(qty),
                f"₱{float(price):,.2f}",
                f"₱{float(subtotal):,.2f}"
            ))

        tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        close_btn = tk.Button(dialog, text="Close", command=dialog.destroy,
                              bg="#95a5a6", fg="white", font=self.normal_font,
                              relief=tk.FLAT, padx=30, pady=10, cursor="hand2")
        close_btn.pack(pady=20)

    def show_cashiers(self):
        """Display cashiers management interface"""
        self.clear_content()
        self.highlight_nav_button(self.btn_cashiers)
        self.current_view = tk.StringVar(value='cashiers')

        title_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        title = tk.Label(title_frame, text="Cashiers Management", font=self.title_font, bg="white", fg="#2c3e50")
        title.pack(side=tk.LEFT)

        refresh_btn = tk.Button(title_frame, text="Refresh", command=self.show_cashiers,
                                bg="#3498db", fg="white", font=self.normal_font,
                                relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        refresh_btn.pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "username", "sales_count", "total_sales")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        tree.heading("id", text="ID")
        tree.heading("name", text="Name")
        tree.heading("username", text="Username")
        tree.heading("sales_count", text="Total Transactions")
        tree.heading("total_sales", text="Total Sales")

        tree.column("id", width=60, anchor="center")
        tree.column("name", width=200, anchor="w")
        tree.column("username", width=150, anchor="w")
        tree.column("sales_count", width=150, anchor="center")
        tree.column("total_sales", width=150, anchor="e")

        query = """
            SELECT c.id, c.name, u.username,
                   COUNT(s.id) as sales_count,
                   COALESCE(SUM(s.total), 0) as total_sales
            FROM cashiers c
            LEFT JOIN users u ON c.user_id = u.id
            LEFT JOIN sales s ON c.id = s.cashier_id AND s.payment_method != 'report'
            GROUP BY c.id, c.name, u.username
            ORDER BY c.name
        """
        results = self.db.execute_query(query, fetch=True)

        if results:
            for row in results:
                cashier_id, name, username, sales_count, total_sales = row
                tree.insert('', 'end', values=(
                    cashier_id,
                    name,
                    username,
                    int(sales_count),
                    f"₱{float(total_sales):,.2f}"
                ))

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

    def show_reports(self):
        """Display reports interface"""
        self.clear_content()
        self.highlight_nav_button(self.btn_reports)
        self.current_view = tk.StringVar(value='reports')

        title_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        title_frame.pack(fill=tk.X)

        title = tk.Label(title_frame, text="Reports & Analytics", font=self.title_font, bg="white", fg="#2c3e50")
        title.pack(anchor="w")

        subtitle = tk.Label(title_frame, text="Generate and view detailed reports",
                            font=self.normal_font, bg="white", fg="#7f8c8d")
        subtitle.pack(anchor="w", pady=(5, 0))

        report_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        report_frame.pack(fill=tk.BOTH, expand=True)

        reports = [
            ("Sales Report", "View detailed sales analytics", self.generate_sales_report),
            ("Inventory Report", "Check stock levels and movements", self.generate_inventory_report),
            ("Cashier Performance", "Analyze cashier productivity", self.generate_cashier_report),
        ]

        for i, (title_text, desc, command) in enumerate(reports):
            card = tk.Frame(report_frame, bg="white", relief=tk.SOLID, bd=1, padx=20, pady=20)
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")

            tk.Label(card, text=title_text, font=self.header_font, bg="white", fg="#2c3e50").pack(anchor="w",
                                                                                                  pady=(0, 10))
            tk.Label(card, text=desc, font=self.normal_font, bg="white", fg="#7f8c8d").pack(anchor="w", pady=(0, 15))

            btn = tk.Button(card, text="Generate Report", command=command,
                            bg="#3498db", fg="white", font=self.normal_font,
                            relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
            btn.pack(anchor="w")

        report_frame.grid_columnconfigure(0, weight=1)
        report_frame.grid_columnconfigure(1, weight=1)

    def generate_sales_report(self):
        """Generate sales report"""
        messagebox.showinfo("Sales Report", "Sales report generation coming soon!")

    def generate_inventory_report(self):
        """Generate inventory report"""
        messagebox.showinfo("Inventory Report", "Inventory report generation coming soon!")

    def generate_cashier_report(self):
        """Generate cashier performance report"""
        messagebox.showinfo("Cashier Report", "Cashier report generation coming soon!")

    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.db.close()
            if self.logout_callback:
                self.logout_callback()