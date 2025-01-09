import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        label = tk.Label(self, text="Welcome to Taif Al-Salmi", font=("Arial", 16), bg="white")
        label.pack(pady=20)

        description = tk.Label(self, text="Select a service from the navigation bar.", bg="white")
        description.pack(pady=10)
