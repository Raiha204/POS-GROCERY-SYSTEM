Nabunturan Grocery Store POS System
A comprehensive Point of Sale (POS) system built with Python and Tkinter for managing grocery store operations. This system features separate interfaces for cashiers and administrators, with real-time inventory management, sales tracking, and reporting capabilities.
Show Image
Show Image
Show Image
Features
Cashier Panel

Point of Sale Interface

Product search and browsing
Shopping cart management
Real-time stock checking
Discount application
Multiple payment methods (Cash/Card)
Automatic change calculation
Receipt printing and reprinting


Dashboard

Daily sales summary
Transaction history
Performance metrics
Items sold tracking


Shift Management

Time-in/Time-out logging
Shift report submission
Activity tracking



Admin Panel

Dashboard

Real-time statistics overview
Today's sales monitoring
Low stock alerts
Recent transactions


Product Management

Add, edit, and delete products
Category organization
Stock level management
Price updates
Search and filter functionality


Sales Management

View all transactions
Filter by date (Today/Week/Month/All)
Detailed sale breakdown
Transaction history


Cashier Management

View cashier performance
Track total transactions
Monitor sales by cashier


Reports & Analytics

Sales reports
Inventory reports
Cashier performance reports



Getting Started
Prerequisites

Python 3.8 or higher
XAMPP (includes Apache and MySQL/MariaDB)
pip (Python package installer)

Installation

Clone the repository

bash   git clone https://github.com/yourusername/nabunturan-grocery-pos.git
   cd nabunturan-grocery-pos

Install required packages

bash   pip install mysql-connector-python

Start XAMPP Services

Open XAMPP Control Panel
Start Apache service
Start MySQL service
Verify both services are running (green indicators)


Set up the database
Open phpMyAdmin (http://localhost/phpmyadmin) and create a database:

Click "New" in the left sidebar
Database name: nabunturan_grocery
Collation: utf8mb4_general_ci
Click "Create"

Or use SQL tab:

sql   CREATE DATABASE nabunturan_grocery;
   USE nabunturan_grocery;

Create the required tables
In phpMyAdmin, select nabunturan_grocery database and go to SQL tab, then paste and execute:

sql   -- Users table
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       role ENUM('admin', 'cashier') NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Cashiers table
   CREATE TABLE cashiers (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       name VARCHAR(100) NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
   );

   -- Products table
   CREATE TABLE products (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       category VARCHAR(50) NOT NULL,
       price DECIMAL(10, 2) NOT NULL,
       stock DECIMAL(10, 2) NOT NULL DEFAULT 0,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Sales table
   CREATE TABLE sales (
       id INT AUTO_INCREMENT PRIMARY KEY,
       cashier_id INT NOT NULL,
       total DECIMAL(10, 2) NOT NULL,
       discount DECIMAL(10, 2) DEFAULT 0,
       payment_method ENUM('cash', 'card', 'report') NOT NULL,
       feedback TEXT,
       date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (cashier_id) REFERENCES cashiers(id)
   );

   -- Sale items table
   CREATE TABLE sale_items (
       id INT AUTO_INCREMENT PRIMARY KEY,
       sale_id INT NOT NULL,
       product_id INT NOT NULL,
       quantity DECIMAL(10, 2) NOT NULL,
       price DECIMAL(10, 2) NOT NULL,
       FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
       FOREIGN KEY (product_id) REFERENCES products(id)
   );

   -- Cashier logs table
   CREATE TABLE cashier_logs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       cashier_id INT NOT NULL,
       activity VARCHAR(100) NOT NULL,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (cashier_id) REFERENCES cashiers(id)
   );

Insert sample data (Optional)
In phpMyAdmin SQL tab, paste and execute:

sql   -- Admin user (username: admin, password: admin123)
   INSERT INTO users (username, password, role) 
   VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');

   -- Cashier user (username: cashier1, password: cashier123)
   INSERT INTO users (username, password, role) 
   VALUES ('cashier1', '6ee4a469cd4e91053847f5d3fcb61dbcc91e8f0ef10be7748da4c4a1ba382d17', 'cashier');

   INSERT INTO cashiers (user_id, name) VALUES (2, 'Justine Nabunturan');

   -- Sample products
   INSERT INTO products (name, category, price, stock) VALUES
   ('Apples 1kg', 'Fruits', 120.00, 20),
   ('Apply', 'Fruits', 40.00, 100),
   ('Bread', 'Bakery', 25.00, 100),
   ('Milk 1L', 'Dairy', 40.00, 100),
   ('Orange', 'Fruits', 30.00, 100),
   ('Rice 5kg', 'Grains', 150.00, 50);

Configure database connection
Edit database.py and update the connection settings:

python   self.connection = mysql.connector.connect(
       host='localhost',
       user='root',
       password='',  # Your MySQL password
       database='nabunturan_grocery',
       autocommit=True
   )

Run the application

bash   python main.py
