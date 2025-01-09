import tkinter as tk
from ui.home_screen import HomeScreen
from ui.passport_screen import PassportScreen
# from ui.visa_screen import VisaScreen
# from ui.ticket_screen import TicketScreen


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Taif Al-Salmi")
        self.geometry("800x600")
        
        # Header (Navigation Bar)
        self.header_frame = tk.Frame(self, bg="blue", height=50)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.current_frame = None  # To track the current screen

        # Create navigation buttons
        self.create_nav_buttons()

        # Start with HomeScreen
        self.show_frame(HomeScreen)

    def create_nav_buttons(self):
        """Creates navigation buttons in the header."""
        home_button = tk.Button(
            self.header_frame, text="Home", bg="blue", fg="white", command=lambda: self.show_frame(HomeScreen)
        )
        home_button.pack(side=tk.LEFT, padx=10, pady=10)

        passport_button = tk.Button(
            self.header_frame, text="Passport", bg="blue", fg="white", command=lambda: self.show_frame(PassportScreen)
        )
        passport_button.pack(side=tk.LEFT, padx=10, pady=10)

        visa_button = tk.Button(
            self.header_frame, text="Visa", bg="blue", fg="white", command=lambda: self.show_frame(VisaScreen)
        )
        visa_button.pack(side=tk.LEFT, padx=10, pady=10)

        ticket_button = tk.Button(
            self.header_frame, text="Ticket", bg="blue", fg="white", command=lambda: self.show_frame(TicketScreen)
        )
        ticket_button.pack(side=tk.LEFT, padx=10, pady=10)

    def show_frame(self, frame_class):
        """Switch between frames (pages)."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
