import tkinter as tk
from ui.adds.add_umrah_screen import AddUmrahScreen
from ui.edits.edit_umrah_screen import EditUmrahScreen
from services.umrah_service import UmrahService
from ui.base_screen import BaseScreen

class UmrahScreen(BaseScreen):
    def __init__(self, master):
        columns = ("ID", "الاسم", "رقم الجواز", "من (تاريخ الدخول)", "إلى (تاريخ الخروج)", "الشركة", "المبلغ", "المبلغ المدفوع", "المتبقي", "  تاريخ الرحلة (عدد الأيام المتبقية)", "الحالة")
        super().__init__(master, UmrahService(master), AddUmrahScreen, EditUmrahScreen, columns)