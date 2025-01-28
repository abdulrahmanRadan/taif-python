import tkinter as tk
from ui.adds.add_ticket_screen import AddTicketScreen
from ui.edits.edit_ticket_screen import EditTicketScreen
from services.ticket_service import TicketService
from ui.base_screen import BaseScreen

class TicketScreen(BaseScreen):
    def __init__(self, master):
        columns = ("ID", "الاسم", "رقم الجواز", "من", "إلى", "الشركة", "المبلغ", "للوكيل", "الصافي", "تاريخ الرحلة", "المكتب", "مدفوع", "المتبقي")
        super().__init__(master, TicketService(master), AddTicketScreen, EditTicketScreen, columns)