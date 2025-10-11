import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from utils import hash_password


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Nabunturan Grocery Store")

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size
        window_width = 500
        window_height = 600

        # Calculate center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set window position and size
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)
        self.root.configure(bg='white')

        # Create main container
        main_frame = tk.Frame(root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left side - Branding section
        left_frame = tk.Frame(main_frame, bg='#2c3e50', width=500)
        left_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)

        # Logo/Icon area
        logo_frame = tk.Frame(left_frame, bg='#2c3e50')
        logo_frame.pack(expand=True, pady=(40, 20))

        # Store icon
        icon_label = tk.Label(logo_frame, text="🏪", font=('Arial', 80), bg='#2c3e50', fg='white')
        icon_label.pack()

        # Store name
        store_name = tk.Label(logo_frame, text="Nabunturan",
                              font=('Arial', 32, 'bold'), bg='#2c3e50', fg='white')
        store_name.pack(pady=(10, 0))

        store_subtitle = tk.Label(logo_frame, text="Grocery Store POS System",
                                  font=('Arial', 14), bg='#2c3e50', fg='#95a5a6')
        store_subtitle.pack()

        # Right side - Login form
        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Welcome text
        welcome_label = tk.Label(right_frame, text="Welcome Back!",
                                 font=('Arial', 24, 'bold'), bg='white', fg='#2c3e50')
        welcome_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(right_frame, text="Please login to your account",
                                  font=('Arial', 11), bg='white', fg='#7f8c8d')
        subtitle_label.pack(pady=(0, 30))

        # Username field
        username_frame = tk.Frame(right_frame, bg='white')
        username_frame.pack(fill=tk.X, pady=(0, 15))

        username_label = tk.Label(username_frame, text="👤 Username",
                                  font=('Arial', 10, 'bold'), bg='white', fg='#34495e')
        username_label.pack(anchor='w', pady=(0, 5))

        self.username_entry = tk.Entry(username_frame, font=('Arial', 12),
                                       relief=tk.SOLID, bd=1, highlightthickness=2,
                                       highlightbackground='#bdc3c7', highlightcolor='#3498db')
        self.username_entry.pack(fill=tk.X, ipady=8)
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())

        # Password field
        password_frame = tk.Frame(right_frame, bg='white')
        password_frame.pack(fill=tk.X, pady=(0, 15))

        password_label = tk.Label(password_frame, text="🔒 Password",
                                  font=('Arial', 10, 'bold'), bg='white', fg='#34495e')
        password_label.pack(anchor='w', pady=(0, 5))

        self.password_entry = tk.Entry(password_frame, show='●', font=('Arial', 12),
                                       relief=tk.SOLID, bd=1, highlightthickness=2,
                                       highlightbackground='#bdc3c7', highlightcolor='#3498db')
        self.password_entry.pack(fill=tk.X, ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login())

        # Role field
        role_frame = tk.Frame(right_frame, bg='white')
        role_frame.pack(fill=tk.X, pady=(0, 25))

        role_label = tk.Label(role_frame, text="👥 Select Role",
                              font=('Arial', 10, 'bold'), bg='white', fg='#34495e')
        role_label.pack(anchor='w', pady=(0, 5))

        # Custom styled combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                        fieldbackground='white',
                        background='white',
                        foreground='#2c3e50',
                        bordercolor='#bdc3c7',
                        arrowcolor='#3498db',
                        padding=8)

        self.role_var = tk.StringVar(value='cashier')
        role_combo = ttk.Combobox(role_frame, textvariable=self.role_var,
                                  values=['admin', 'cashier'],
                                  state='readonly', font=('Arial', 12),
                                  style='Custom.TCombobox')
        role_combo.pack(fill=tk.X)

        # Login button with hover effect
        self.login_btn = tk.Button(right_frame, text="LOGIN", command=self.login,
                                   bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                   relief=tk.FLAT, cursor='hand2', activebackground='#2980b9',
                                   activeforeground='white')
        self.login_btn.pack(fill=tk.X, ipady=12, pady=(10, 0))

        # Add hover effects
        self.login_btn.bind('<Enter>', lambda e: self.login_btn.config(bg='#2980b9'))
        self.login_btn.bind('<Leave>', lambda e: self.login_btn.config(bg='#3498db'))

        # Footer
        footer_label = tk.Label(right_frame, text="© 2025 Nabunturan Grocery Store",
                                font=('Arial', 9), bg='white', fg='#95a5a6')
        footer_label.pack(side=tk.BOTTOM, pady=(20, 0))

        # Focus on username entry
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password_input = self.password_entry.get()
        role = self.role_var.get()

        # Validation
        if not username:
            messagebox.showerror("Login Error", "Please enter your username!")
            self.username_entry.focus()
            return

        if not password_input:
            messagebox.showerror("Login Error", "Please enter your password!")
            self.password_entry.focus()
            return

        # Disable login button during authentication
        self.login_btn.config(state='disabled', text='LOGGING IN...')
        self.root.update()

        try:
            password = hash_password(password_input)
            db = Database()

            query = """
                SELECT u.id, u.username, c.name 
                FROM users u 
                LEFT JOIN cashiers c ON u.id = c.user_id 
                WHERE u.username = %s AND u.password = %s AND u.role = %s
            """
            result = db.execute_query(query, (username, password, role), fetch=True)

            if result:
                user_id, username, name = result[0]

                if role == 'cashier':
                    # Fetch cashier_id
                    cashier_query = "SELECT id FROM cashiers WHERE user_id = %s"
                    cashier_id = db.execute_query(cashier_query, (user_id,), fetch=True)
                    cashier_id_val = cashier_id[0][0] if cashier_id and cashier_id[0] else None

                    if not cashier_id_val:
                        messagebox.showerror("Login Error", "Cashier profile not found!")
                        db.close()
                        self.login_btn.config(state='normal', text='LOGIN')
                        return

                    # Log time-in
                    log_query = "INSERT INTO cashier_logs (cashier_id, activity) VALUES (%s, 'Time-in')"
                    db.execute_query(log_query, (cashier_id_val,))

                    db.close()
                    self.root.destroy()

                    # Import and create CashierWindow
                    from cashier_window import CashierWindow
                    CashierWindow(user_id, name, cashier_id_val)

                else:  # admin
                    db.close()
                    self.root.destroy()

                    # Import and create AdminWindow
                    from admin_window import AdminWindow
                    admin_root = tk.Tk()

                    def logout_callback():
                        admin_root.destroy()
                        # Reopen login
                        login_root = tk.Tk()
                        LoginWindow(login_root)
                        login_root.mainloop()

                    AdminWindow(admin_root, name, logout_callback)
                    admin_root.mainloop()
            else:
                db.close()
                messagebox.showerror("Login Failed",
                                     "Invalid username, password, or role.\nPlease check your credentials and try again.")
                self.login_btn.config(state='normal', text='LOGIN')
                self.password_entry.delete(0, tk.END)
                self.username_entry.focus()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during login:\n{str(e)}")
            self.login_btn.config(state='normal', text='LOGIN')
            print(f"Login error: {str(e)}")