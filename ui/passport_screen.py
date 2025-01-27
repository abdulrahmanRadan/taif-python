import tkinter as tk
from ui.adds.add_passport_screen import AddPassportScreen
from ui.edits.edit_passport_screen import EditPassportScreen
from services.passport_service import PassportService
from ui.base_screen import BaseScreen

class PassportScreen(BaseScreen):
    def __init__(self, master):
        columns = ("ID", "الاسم", "تاريخ الحجز", "نوع الجواز", "سعر الحجز", "سعر الشراء", "الصافي", "المبلغ المدفوع", "المبلغ المتبقي", "حالة الجواز", "تاريخ الاستلام", "اسم المستلم")
        super().__init__(master, PassportService(master), AddPassportScreen, EditPassportScreen, columns)