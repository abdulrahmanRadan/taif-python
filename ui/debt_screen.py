import tkinter as tk
from tkinter import ttk
from services.debt_service import DebtService
from ui.adds.add_ticket_screen import AddTicketScreen
from ui.edits.edit_ticket_screen import EditTicketScreen
from services.ticket_service import TicketService
from ui.base_screen import BaseScreen



class DebtScreen(BaseScreen):
    def __init__(self, master):
        columns = ("ID", "الاسم", "رقم الجواز", "من", "إلى", "الشركة", "المبلغ", "للوكيل", "الصافي", "تاريخ الرحلة", "المكتب")
        super().__init__(master, DebtService(master), AddTicketScreen, EditTicketScreen, columns )
        