from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from services.validator import Validator

class PassportService:
    def __init__(self, master):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
        self.validator = Validator()
        self.master = master

    def add_passport_data(self, data):
        columns = [
            "name", "booking_date", "type", "booking_price", "purchase_price",
            "net_amount", "paid_amount", "remaining_amount", "status", "receipt_date", "receiver_name", "currency"
        ]
        data_dict = dict(zip(columns, data[1:]))

        rules = {
            "name": ["required", "min:3", "max:50"],
            "booking_date": ["required"],
            "type": ["required"],
            "booking_price": [ "numeric:2"],
            "purchase_price": [ "numeric:2"],
            "net_amount": [ "numeric:2"],
            "paid_amount": ["numeric:2"],
            "remaining_amount": ["numeric:2"],
            "status": ["required"],
            "currency": ["required"]
        }

        if self.validator.validate(data_dict, rules):
            self.db_manager.insert("Passports", **data_dict)
            return True, "تمت إضافة البيانات بنجاح."
        else:
            errors = self.validator.get_errors()
            return False, "\n".join([f"{field}: {', '.join(errs)}" for field, errs in errors.items()])

    def format_currency(self, currency_code):
        """
        تحويل رمز العملة المخزن في قاعدة البيانات إلى نص.
        """
        currency_map = {"1": "ر.ي", "2": "ر.س", "3": "دولار"}
        return currency_map.get(currency_code, "ر.ي")  # افتراضيًا ر.ي إذا لم يتم العثور على الرمز

    def format_status(self, status_code):
        """
        تحويل رمز حالة الجواز المخزن في قاعدة البيانات إلى نص.
        """
        status_map = {"1": "في الطابعة", "2": "في المكتب", "3": "تم الاستلام", "4": "مرفوض"}
        return status_map.get(status_code, "غير معروف")

    def format_type(self, type_code):
        """
        تحويل رمز نوع الجواز المخزن في قاعدة البيانات إلى نص.
        """
        type_map = {"1": "عادي", "2": "مستعجل عدن", "3": "مستعجل بيومه", "4": "غير ذلك"}
        return type_map.get(type_code, "غير معروف")

    def merge_currency_with_amounts(self, row):
        """
        دمج نص العملة مع قيم الأعمدة المالية.
        """
        currency_text = self.format_currency(row[11])  # تحويل رمز العملة إلى نص
        row = list(row)
        row[4] = f"{row[4]} {currency_text}"  # booking_price
        row[5] = f"{row[5]} {currency_text}"  # purchase_price
        row[6] = f"{row[6]} {currency_text}"  # net_amount
        row[7] = f"{row[7]} {currency_text}"  # paid_amount
        row[8] = f"{row[8]} {currency_text}"  # remaining_amount
        return tuple(row)

    def get_all_data(self):
        """
        استرجاع جميع البيانات من قاعدة البيانات.
        """
        data = self.db_manager.select("Passports")
        formatted_data = []
        for row in data:
            row = list(row)
            row[3] = self.format_type(row[3])  # تحويل نوع الجواز
            row[9] = self.format_status(row[9])  # تحويل حالة الجواز
            formatted_row = self.merge_currency_with_amounts(row)  # دمج العملة مع الأعمدة
            formatted_data.append(formatted_row[:12])  # إزالة العمود رقم 11 (العملة)
        return formatted_data

    def search_data(self, search_term: str):
        """
        البحث في قاعدة البيانات باستخدام مصطلح البحث.
        """
        if not search_term:
            return self.get_all_data()

        # البحث في الأعمدة "name" و "receiver_name"
        results = self.search_manager.search("Passports", ["name", "receiver_name", "status", "type"], search_term)
        formatted_data = []
        for row in results:
            row = list(row.values())
            row[3] = self.format_type(row[3])  # تحويل نوع الجواز
            row[9] = self.format_status(row[9])  # تحويل حالة الجواز
            formatted_row = self.merge_currency_with_amounts(row)  # دمج العملة مع الأعمدة
            formatted_data.append(formatted_row[:12])  # إزالة العمود رقم 12 (العملة)
        return formatted_data

    def export_to_pdf(self):
        print("Export to PDF - Functionality not implemented yet.")

    def export_to_excel(self):
        print("Export to Excel - Functionality not implemented yet.")

    def save_passport_data(self, data, master):
        success, message = self.add_passport_data(data)
        if success:
            master.add_to_table(data)
        return success, message