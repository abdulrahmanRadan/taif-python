from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from services.validator import Validator


class DebtService:
    def __init__(self, master):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
        self.validator = Validator()


    def add_data(self, data):
        columns = [
            "name", "type", "date", "ry_price", "rs_price", "paid_amount", "type_paid"
        ]
        data_dict=dict(zip(columns, data[1:]))

        rules = {
            "name": ["required", "min:3", "max:50"],
            "type": ["required"],
            "date": [ "date"],
            "paid_amount": ["numeric:2"],
            "ry_price": ["numeric:2"],
            "rs_price": ["numeric:2"],
            "type_paid": ["required"]
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



    def get_all_data(self):
        """
        استرجاع جميع الديون من جميع الجداول.
        """
        debts = []

        # استرجاع الديون من جدول Passports
        passports_debts = self.db_manager.select_with_condition("Passports", "remaining_amount > 0")
        for debt in passports_debts:
            debts.append({
                "id": debt[0],
                "name": debt[1],
                "service": "جواز سفر",
                "date": debt[2],
                "amount_yemeni": debt[8] if debt[12] == "1" else 0,
                "amount_saudi": debt[8] if debt[12] == "2" else 0,
                "received": debt[7],
                "received_date": debt[10],
                "received_type": "نقدي"  # يمكن تعديله حسب الحاجة
            })

        # استرجاع الديون من جدول Umrah
        umrah_debts = self.db_manager.select_with_condition("Umrah", "remaining_amount > 0")
        for debt in umrah_debts:
            debts.append({
                "id": debt[0],
                "name": debt[1],
                "service": "عمرة",
                "date": debt[9],
                "amount_yemeni": debt[8] if debt[12] == "1" else 0,
                "amount_saudi": debt[8] if debt[12] == "2" else 0,
                "received": debt[7],
                "received_date": debt[10],
                "received_type": "نقدي"  # يمكن تعديله حسب الحاجة
            })

        # استرجاع الديون من جدول Trips
        trips_debts = self.db_manager.select_with_condition("Trips", "remaining_amount > 0")
        for debt in trips_debts:
            debts.append({
                "id": debt[0],
                "name": debt[1],
                "service": "رحلة",
                "date": debt[10],
                "amount_yemeni": debt[8] if debt[7] == "1" else 0,
                "amount_saudi": debt[8] if debt[7] == "2" else 0,
                "received": debt[6],
                "received_date": debt[10],
                "received_type": "نقدي"  # يمكن تعديله حسب الحاجة
            })

        # ترتيب الديون حسب التاريخ
        debts.sort(key=lambda x: x["date"])

        return debts

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

    
    def get_by_id(self, passport_id):
        """
        جلب بيانات جواز السفر من قاعدة البيانات باستخدام id.
        """
        query = "SELECT * FROM Passports WHERE id = ?"
        result = self.db_manager.execute_read_query(query, (passport_id,))
        if result:
            return result[0]  # إرجاع الصف الأول (يجب أن يكون هناك صف واحد فقط)
        return None
        
    def export_to_excel(self):
        export_screen = PassportsExporter(self.master)
        # print("Export to Excel - Functionality not implemented yet.")

    def save_passport_data(self, data, master):
        success, message = self.add_passport_data(data)
        if success:
            master.add_to_table(data)
        return success, message


    def update_passport_data(self, data, master):
        """
        تحديث بيانات جواز السفر في قاعدة البيانات.
        """
        try:
            # تحويل البيانات إلى قاموس
            updated_data = {
                "name": data[1],
                "booking_date": data[2],
                "type": data[3],
                "booking_price": data[4],
                "purchase_price": data[5],
                "net_amount": data[6],
                "paid_amount": data[7],
                "remaining_amount": data[8],
                "status": data[9],
                "receipt_date": data[10],
                "receiver_name": data[11],
                "currency": data[12]
            }

            # تحديث البيانات في قاعدة البيانات
            self.db_manager.update("Passports", data[0], **updated_data)
            return True, "تم تحديث البيانات بنجاح!"
        except Exception as e:
            return False, f"حدث خطأ أثناء تحديث البيانات: {str(e)}"

    def mark_debt_as_paid(self, debt_id, service_type):
        """
        تحديث حالة الدين إلى مدفوع.
        """
        try:
            if service_type == "جواز سفر":
                self.db_manager.update("Passports", debt_id, remaining_amount=0)
            elif service_type == "عمرة":
                self.db_manager.update("Umrah", debt_id, remaining_amount=0)
            elif service_type == "رحلة":
                self.db_manager.update("Trips", debt_id, remaining_amount=0)
            return True, "تم تحديث حالة الدين إلى مدفوع."
        except Exception as e:
            return False, f"حدث خطأ أثناء تحديث حالة الدين: {str(e)}"