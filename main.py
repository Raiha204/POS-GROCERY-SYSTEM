"""
Nabunturan Grocery Store POS System
Main Entry Point

This is the main file that launches the application.
Run this file to start the POS system.
"""

import tkinter as tk
from login_window import LoginWindow
from database import Database


def main():
    """
    Main function to run the Nabunturan Grocery Store POS System
    """
    # Create the main root window
    root = tk.Tk()

    # Initialize the login window
    app = LoginWindow(root)

    # Ensure database connection is closed when the main window is closed
    def on_closing():
        """Handle application closing"""
        try:
            db = Database()
            db.close()
        except:
            pass
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    # Entry point of the application
    print("=" * 50)
    print("Nabunturan Grocery Store POS System")
    print("Initializing application...")
    print("=" * 50)

    main()