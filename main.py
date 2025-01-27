import tkinter as tk
from ui.home_screen import HomeScreen
from ui.passport_screen import PassportScreen
from ui.UmrahScreen import UmrahScreen
from ui.TicketScreen import TicketScreen
from ui.User.login_screen import LoginScreen

# database
from database.database_manager import DatabaseManager



class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.withdraw()  # إخفاء النافذة الرئيسية في البداية
        
        # إنشاء نافذة تسجيل الدخول
        # self.login_screen = LoginScreen(self)
        # self.login_screen.grab_set()

        self.title("مكتب طائف السالمي")
        self.geometry("800x600")
        
        # Header (Navigation Bar)
        self.header_frame = tk.Frame(self, bg="#38B6A5", height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        # اسم التطبيق
        app_name_label = tk.Label(
            self.header_frame,
            text="مكتب طائف السالمي",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#38B6A5"
        )
        app_name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.current_frame = None  # To track the current screen
        self.active_button = None  # To track the active button

        # Create navigation buttons
        self.create_nav_buttons()

        # Start with HomeScreen
        self.show_frame(HomeScreen, self.home_button)

        # database check
        self.connect_database()
    
    def connect_database(self):
        # database check
        db_manager = DatabaseManager()
        # Tables are created upon initialization
        # Additional setup code can be added here
        db_manager.close()
        print("Connected to database successfully")

    def create_nav_buttons(self):
        """Creates navigation buttons in the header."""
        # Configure the header frame to use grid layout
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)
        self.header_frame.grid_columnconfigure(3, weight=1)
        self.header_frame.grid_columnconfigure(4, weight=1)
        self.header_frame.grid_columnconfigure(5, weight=1)

        # Define button styles
        button_style = {
            "bg": "#1F7B6F",  # لون الخلفية الافتراضي
            "fg": "white",    # لون النص
            "font": ("Arial", 12, "bold"),  # نوع الخط وحجمه
            "relief": "flat",  # إزالة الحواف الافتراضية
            "borderwidth": 0,  # إزالة الحدود
            "activebackground": "#1C727D",  # لون الخلفية عند النقر
            "padx": 10,
            "pady": 5
        }

        # Home Button
        self.home_button = tk.Button(
            self.header_frame, text="الصفحة الرئيسية", **button_style, command=lambda: self.show_frame(HomeScreen, self.home_button)
        )
        self.home_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

        # Passport Button
        self.passport_button = tk.Button(
            self.header_frame, text="الجوازات", **button_style, command=lambda: self.show_frame(PassportScreen, self.passport_button)
        )
        self.passport_button.grid(row=0, column=2, sticky="nsew", padx=5, pady=10)

        # Umrah Button
        self.umrah_button = tk.Button(
            self.header_frame, text="العمرة", **button_style, command=lambda: self.show_frame(UmrahScreen, self.umrah_button)
        )
        self.umrah_button.grid(row=0, column=3, sticky="nsew", padx=5, pady=10)
        
        # Ticket Button
        self.ticket_button = tk.Button(
            self.header_frame, text="الحجوزات", **button_style, command=lambda: self.show_frame(TicketScreen, self.ticket_button)
        )
        self.ticket_button.grid(row=0, column=4, sticky="nsew", padx=5, pady=10)
        
        # debts Button
        self.debts_button = tk.Button(
            self.header_frame, text="الديون", **button_style
        )
        self.debts_button.grid(row=0, column=5, sticky="nsew", padx=5, pady=10)

    def show_frame(self, frame_class, button):
        """Switch between frames (pages) and highlight the active button."""
        if self.current_frame:
            self.current_frame.destroy()
        
        # Reset the color of the previously active button
        if self.active_button:
            self.active_button.config(bg="#1F7B6F")  # العودة إلى اللون الافتراضي

        # Set the new active button
        self.active_button = button
        self.active_button.config(bg="#17A8A1")  # تغيير لون الزر النشط

        # Show the new frame
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()