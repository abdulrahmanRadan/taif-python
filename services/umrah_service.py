from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from services.validator import Validator 


class UmrahService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.validator = Validator()  # تهيئة Validator

    def add_umrah_data(self, data):
        """إضافة بيانات معتمر جديدة."""
        columns = [
            "name", "passport_number", "phone_number", "sponsor_name",
            "sponsor_number", "cost", "paid", "remaining_amount",
            "entry_date", "exit_date", "days_left", "status"
        ]
        # self.data.append(data)
        data_dict = dict(zip(columns, data[1:]))  # convert data into dictionary
        rules = {
            "name": ["required", "min:3", "max:50", "string"],
            "passport_number": ["required", "min:8", "max:20", "string"],
            "phone_number": [ "min:8",  "phone"],
            "sponsor_name": [ "string"],
            "sponsor_number": ["phone"],
            "cost": ["required", "numeric"],
            "paid": ["required", "numeric"],
            "remaining_amount": ["required", "numeric"],
            "entry_date": ["required"],
            "exit_date": ["required"],
            "status": ["required"]
        }
        
        # التحقق من صحة البيانات
        if self.validator.validate(data_dict, rules):
            self.db_manager.insert("Umrah", **data_dict)
            return True, "تمت إضافة البيانات بنجاح."
        else:
            errors = self.validator.get_errors()
            error_message = "فشل التحقق من البيانات:\n"
            for field, field_errors in errors.items():
                error_message += f"- {field}: {', '.join(field_errors)}\n"
            return False, error_message

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
        # data = [
        #     (1, "محمد أحمد", "A12345678", "0123456789", "علي محمد", "987654321", "5000", "3000", "2000", "2023-11-01", "2023-11-10", "5", "مهم"),
        #     (2, "فاطمة علي", "B87654321", "0987654321", "حسن أحمد", "123456789", "6000", "4000", "2000", "2023-11-05", "2023-11-15", "10", "غير مهم"),
        # ]
        # return data
        return self.db_manager.select("Umrah")

    def export_to_pdf(self):
        """تصدير البيانات إلى PDF."""
        print("Export to PDF - Functionality not implemented yet.")

    def export_to_excel(self):
        """تصدير البيانات إلى Excel."""
        print("Export to Excel - Functionality not implemented yet.")

    def save_umrah_data(self, data, master):
        """حفظ بيانات المعتمر وإضافتها إلى الجدول."""
        success, message = self.add_umrah_data(data)
        if success:
            master.add_to_table(data)
        return success, message