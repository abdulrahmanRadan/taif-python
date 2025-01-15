from datetime import datetime
from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from services.validator import Validator 

class UmrahService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
        self.validator = Validator()  # تهيئة Validator

    def add_umrah_data(self, data):
        """إضافة بيانات معتمر جديدة."""
        columns = [
            "name", "passport_number", "phone_number", "sponsor_name",
            "sponsor_number", "cost", "paid", "remaining_amount",
            "entry_date", "exit_date", "status"
        ]
        data_dict = dict(zip(columns, data[1:]))  # تحويل البيانات إلى قاموس
        rules = {
            "name": ["required", "min:3", "max:50", "string"],
            "passport_number": ["required", "min:8", "max:20", "string"],
            "phone_number": ["required", "phone:9"],
            "sponsor_name": ["string"],
            "sponsor_number": ["phone:9"],
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

    def calculate_days_left(self, entry_date, exit_date):
        """حساب الأيام المتبقية بناءً على تاريخ الدخول وتاريخ الخروج."""
        try:
            entry_date = str(entry_date)
            exit_date = str(exit_date)
            
            entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
            exit_date = datetime.strptime(exit_date, "%Y-%m-%d").date()
            today = datetime.now().date()

            if entry_date <= today:  # إذا كان تاريخ الدخول قد مر
                days_left = (exit_date - today).days
            else:  # إذا كان تاريخ الدخول في المستقبل
                days_left = (exit_date - entry_date).days

            return max(days_left, 0)  # تجنب القيم السالبة
        except ValueError as e:
            print(f"Error calculating days left: {e}")
            return 0

    def get_all_data(self):
        """الحصول على جميع بيانات المعتمرين مع حساب عدد الأيام المتبقية."""
        data = self.db_manager.select("Umrah")
        updated_data = []
        for record in data:
            # تحويل البيانات إلى قائمة لتعديلها
            record_list = list(record)
            # حساب عدد الأيام المتبقية
            days_left = self.calculate_days_left(record_list[9], record_list[10])  # تاريخ الدخول (8) وتاريخ الخروج (9)
            # إضافة عدد الأيام المتبقية إلى السجل
            # print(days_left)
            record_list.append(days_left)
            updated_data.append(tuple(record_list))
        return updated_data

    def search_data(self, search_term: str):
        """
        البحث في قاعدة البيانات باستخدام مصطلح البحث.
        """
        if not search_term:
            return self.get_all_data()
        # the table "name", "passport_number", "phone_number", "sponsor_number", "sponsor_name"
        results = self.search_manager.search("Umrah", ["name", "passport_number", "phone_number","sponsor_number", "sponsor_name"], search_term)
        formatted_data = []
        for row in results:
            row_data = list(row.values())
            days_left = self.calculate_days_left(row_data[9], row_data[10])
            row_data.append(days_left)
            formatted_data.append(tuple(row_data))
        return formatted_data

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