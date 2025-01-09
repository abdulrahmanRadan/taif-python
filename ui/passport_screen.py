import tkinter as tk
from tkinter import ttk

class PassportScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        # Search and Add New Section
        self.create_top_section()

        # Data Table
        self.create_table_section()

    def create_top_section(self):
        """Create search bar, add new button, and export buttons."""
        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill=tk.X, pady=10, padx=10)

        # Search Bar
        search_label = tk.Label(top_frame, text="Search:", font=("Arial", 12), bg="white")
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        search_entry = tk.Entry(top_frame, font=("Arial", 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Add New Button
        add_button = tk.Button(top_frame, text="Add New", bg="blue", fg="white", font=("Arial", 12), command=self.add_new)
        add_button.pack(side=tk.LEFT, padx=(0, 10))

        # Export Buttons
        export_pdf_button = tk.Button(top_frame, text="Export to PDF", bg="green", fg="white", font=("Arial", 12), command=self.export_to_pdf)
        export_pdf_button.pack(side=tk.LEFT, padx=(0, 5))

        export_excel_button = tk.Button(top_frame, text="Export to Excel", bg="green", fg="white", font=("Arial", 12), command=self.export_to_excel)
        export_excel_button.pack(side=tk.LEFT)

    def create_table_section(self):
        """Create a table to display data."""
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Scrollbars
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # Table
        self.table = ttk.Treeview(
            table_frame, columns=("ID", "Name", "Passport Number", "Status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, show="headings"
        )

        # Configure Scrollbars
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Define Columns
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Passport Number", text="Passport Number")
        self.table.heading("Status", text="Status")

        self.table.column("ID", width=50)
        self.table.column("Name", width=200)
        self.table.column("Passport Number", width=150)
        self.table.column("Status", width=100)

        self.table.pack(fill=tk.BOTH, expand=True)

        # Dummy Data
        self.populate_table()

    def populate_table(self):
        """Populate the table with dummy data."""
        data = [
            (1, "John Doe", "P1234567", "Valid"),
            (2, "Jane Smith", "P7654321", "Expired"),
            (3, "Ali Ahmed", "P2345678", "Valid"),
            (4, "Fatima Khan", "P8765432", "Pending"),
        ]

        for item in data:
            self.table.insert("", tk.END, values=item)

    def add_new(self):
        """Handle adding a new record."""
        print("Add New Record - Functionality not implemented yet.")

    def export_to_pdf(self):
        """Handle exporting data to PDF."""
        print("Export to PDF - Functionality not implemented yet.")

    def export_to_excel(self):
        """Handle exporting data to Excel."""
        print("Export to Excel - Functionality not implemented yet.")
