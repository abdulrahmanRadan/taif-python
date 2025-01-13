from datetime import datetime, timedelta

class UmrahService:
    def __init__(self):
        self.data = []  # قائمة لتخزين بيانات المعتمرين

    def add_umrah_data(self, data):
        """إضافة بيانات معتمر جديدة."""
        self.data.append(data)

    def calculate_remaining_amount(self, cost, paid):
        """حساب المبلغ المتبقي."""
        try:
            return float(cost) - float(paid)
        except ValueError:
            return 0.00

    def calculate_days_left(self, entry_date):
        """حساب الأيام المتبقية حتى تاريخ الدخول."""
        try:
            entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
            today = datetime.now()
            delta = entry_date - today
            return delta.days
        except ValueError:
            return 0

    def get_all_data(self):
        """الحصول على جميع بيانات المعتمرين."""
        data = [
            (1, "محمد أحمد", "A12345678", "0123456789", "علي محمد", "987654321", "5000", "3000", "2000", "2023-11-01", "2023-11-10", "5", "مهم"),
            (2, "فاطمة علي", "B87654321", "0987654321", "حسن أحمد", "123456789", "6000", "4000", "2000", "2023-11-05", "2023-11-15", "10", "غير مهم"),
        ]
        return data

    def export_to_pdf(self):
        """تصدير البيانات إلى PDF."""
        print("Export to PDF - Functionality not implemented yet.")

    def export_to_excel(self):
        """تصدير البيانات إلى Excel."""
        print("Export to Excel - Functionality not implemented yet.")

    def save_umrah_data(self, data, master):
        """حفظ بيانات المعتمر وإضافتها إلى الجدول."""
        self.add_umrah_data(data)
        master.add_to_table(data)