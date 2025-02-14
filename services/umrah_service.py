from datetime import datetime
from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from services.validator import Validator 
from reports.umrah_exporter import UmrahExporter
from datetime import date


class UmrahService:
    def __init__(self, master):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
        self.validator = Validator()  # تهيئة Validator
        self.master = master

    def add_umrah_data(self, data):
        """إضافة بيانات معتمر جديدة."""
        columns = [
            "name", "passport_number", "phone_number", "sponsor_name",
            "sponsor_number", "cost", "paid", "remaining_amount",
            "entry_date", "exit_date", "status", "currency"
        ]
        data_dict = dict(zip(columns, data[1:]))  # تحويل البيانات إلى قاموس
        rules = {
            "name": ["required", "min:3", "max:50", "string"],
            "passport_number": ["required", "min:8", "max:20", "string"],
            "phone_number": ["required", "phone:9"],
            "sponsor_name": ["string"],
            "sponsor_number": ["phone:9"],
            "entry_date": ["required"],
            "exit_date": ["required"],
            "status": ["required"],
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
        """حساب الأيام المتبقية بناءً على تاريخ الدخول وتاريخ الخروج فقط."""
        try:
            # تحويل التواريخ إلى نص (في حال لم تكن نصوصًا)
            entry_date = str(entry_date)
            exit_date = str(exit_date)
            today = date.today()
            
            # تحويل التواريخ إلى كائنات من نوع date
            entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
            exit_date = datetime.strptime(exit_date, "%Y-%m-%d").date()
            # print("entry_date" , entry_date)
            # print("exit_date" , exit_date)

            # حساب الفرق بين تاريخ الخروج وتاريخ الدخول

            days_left = (exit_date - today).days
            # print(days_left)

            # تجنب القيم السالبة (إذا كان تاريخ الخروج قبل تاريخ الدخول)
            return max(days_left, 0)
        except ValueError as e:
            print(f"Error calculating days left: {e}")
            return 0

    def format_currency(self, currency_code):
        """
        تحويل رمز العملة المخزن في قاعدة البيانات إلى نص.
        """
        currency_map = {"1": "ر.ي", "2": "ر.س", "3": "دولار"}
        return currency_map.get(currency_code, "ر.ي")  # افتراضيًا ر.ي إذا لم يتم العثور على الرمز

    def merge_currency_with_amounts(self, row):
        """
        دمج نص العملة مع قيم الأعمدة "cost"، "paid"، و"remaining_amount".
        """
        currency_text = self.format_currency(row[12])  # تحويل رمز العملة إلى نص
        row = list(row)
        row[6] = f"{row[6]} {currency_text}"  # cost
        row[7] = f"{row[7]} {currency_text}"  # paid
        row[8] = f"{row[8]} {currency_text}"  # remaining_amount
        return tuple(row)

    def get_all_data(self):
        """الحصول على جميع بيانات المعتمرين مع تعديل ترتيب الأعمدة لعرضها بشكل صحيح."""
        data = self.db_manager.select("Umrah")
        updated_data = []
        
        for record in data:
            record_list = list(record)
            
            # حساب عدد الأيام المتبقية
            days_left = self.calculate_days_left(record_list[9], record_list[10])
            
            # تنسيق بيانات المعتمر لتتوافق مع الأعمدة المطلوبة
            formatted_row = (
                record_list[0],   # ID
                record_list[1],   # الاسم
                record_list[2],   # رقم الجواز
                record_list[9],   # من (تاريخ الدخول)
                record_list[10],  # إلى (تاريخ الخروج)
                record_list[4],   # الشركة (اسم الضامن)
                f"{record_list[6]} {self.format_currency(record_list[12])}",  # المبلغ (التكلفة)
                f"{record_list[7]} {self.format_currency(record_list[12])}",  # للوكيل (المدفوع)
                f"{record_list[8]} {self.format_currency(record_list[12])}",  # الصافي (المتبقي)
                days_left,        # تاريخ الرحلة (عدد الأيام المتبقية)
                record_list[11]  # المكتب (العملة)
            )
            
            updated_data.append(formatted_row)
        
        return updated_data


    def search_data(self, search_term: str):
        """
        البحث في قاعدة البيانات باستخدام مصطلح البحث.
        """
        if not search_term:
            return self.get_all_data()
        
        # البحث في الأعمدة التالية: "name", "passport_number", "phone_number", "sponsor_number", "sponsor_name"
        results = self.search_manager.search("Umrah", ["name", "passport_number", "phone_number", "sponsor_number", "sponsor_name"], search_term)
        formatted_data = []
        for row in results:
            row_data = list(row.values())
            
            # دمج العملة مع الأعمدة المالية (cost, paid, remaining_amount)
            formatted_row = self.merge_currency_with_amounts(row_data)
            
            # حذف العمود الأخير (currency) بعد دمجه مع الأعمدة الأخرى
            formatted_row = list(formatted_row[:-1])  # تحويل tuple إلى list وإزالة آخر عنصر (currency)
            
            # حساب عدد الأيام المتبقية
            days_left = self.calculate_days_left(formatted_row[9], formatted_row[10])
            
            # إضافة عدد الأيام المتبقية إلى السجل
            formatted_row.append(days_left)
            
            formatted_data.append(formatted_row)
        return formatted_data

    def export_to_excel(self):
        """تصدير البيانات إلى Excel."""
        export_screen = UmrahExporter(self.master)

    def save_umrah_data(self, data, master):
        """حفظ بيانات المعتمر وإضافتها إلى الجدول."""
        success, message = self.add_umrah_data(data)
        if success:
            master.refresh_table()
        return success, message

    def get_by_id(self, umrah_id):
        query = self.db_manager.select("Umrah", id=umrah_id)
        if query:
            return query[0]
        return None

    def update_umrah_data(self, data, master):
        """
        تحديث بيانات رحلات السفر في قاعدة البيانات.
        """
        try:
            update_data = {
                "name": data[1],  # اسم المعتمر
                "passport_number": data[2],  # رقم الجواز
                "phone_number": data[3],  # رقم الهاتف
                "sponsor_name": data[4],  # اسم الضمين
                "sponsor_number": data[5],  # رقم الضمين
                "cost": data[6],  # التكلفة
                "paid": data[7],  # المبلغ المدفوع
                "remaining_amount": data[8],  # المبلغ المتبقي
                "entry_date": data[9],  # تاريخ الدخول
                "exit_date": data[10],  # تاريخ الخروج
                "status": data[11],  # الحالة
                "currency": data[12],  # العملة
            }

            # تحديث البيانات في قاعدة البيانات
            self.db_manager.update("Umrah", data[0], **update_data)
            return True, "تم تحديث البيانات بنجاح!"
        except Exception as e:
            return False, f"حدث خطأ أثناء تحديث البيانات: {str(e)}"

    def delete_data(self, id):
        """
        حذف بيانات جواز السفر من قاعدة البيانات باستخدام id.
        """
        try:
            self.db_manager.delete("Umrah", id=id)
            return True, "تم حذف البيانات بنجاح!"
        except Exception as e:
            return False, f"حدث خطأ أثناء حذف البيانات: {str(e)}"

#