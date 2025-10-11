"""
Database Connection Module for Nabunturan Grocery Store POS System

Handles all database operations using MySQL connection.
"""

import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        """Initialize database connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',  # Change this to your MySQL password if you have one
                database='nabunturan_grocery',
                autocommit=True  # Auto-commit transactions
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Database connection error: {e}")
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=None, fetch=False):
        """
        Execute a database query

        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for parameterized query
            fetch (bool): Whether to fetch results

        Returns:
            list: Query results if fetch=True, True/False for execute operations
        """
        if not self.connection or not self.cursor:
            print("No database connection")
            return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if fetch:
                results = self.cursor.fetchall()
                return results
            else:
                self.connection.commit()
                return True
        except Error as e:
            print(f"Query execution error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            return None

    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()

if __name__ == "__main__":
            db = Database()
            if db.connection and db.connection.is_connected():
                print("Database connection successful!")
                # Test a simple query
                result = db.execute_query("SELECT DATABASE();", fetch=True)
                print(f"Connected to database: {result[0][0]}")
                db.close()
            else:
                print("Failed to connect to database")