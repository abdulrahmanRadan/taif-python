from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from services.validator import Validator
from datetime import datetime


class DebtService:
    def __init__(self, master):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
        self.validator = Validator()

    def add_payment(self, debt_type, debt_id, amount, date, method):
        """
        إضافة دفعة جديدة وتحديث المبالغ المتبقية.
        """
        # إضافة الدفع إلى جدول المدفوعات
        self.db_manager.insert("Payments",
            debt_type=debt_type,
            debt_id=debt_id,
            amount=amount,
            payment_date=date,
            payment_method=method
        )
        
        # تحديث المبالغ المدفوعة والمتبقية في الجدول الأصلي
        table = debt_type
        current = self.db_manager.select(table, id=debt_id)[0]
        new_paid = current[7] + amount  # paid_amount
        new_remaining = current[8] - amount  # remaining_amount
        
        self.db_manager.update(table, debt_id,
            paid_amount=new_paid,
            remaining_amount=new_remaining
        )

    def get_payments(self, debt_type, debt_id):
        """
        استرجاع جميع المدفوعات المرتبطة بدين معين.
        """
        return self.db_manager.select("Payments",
            debt_type=debt_type,
            debt_id=debt_id
        )
    
    def format_currency(self, currency_code):
        """
        تحويل رمز العملة المخزن في قاعدة البيانات إلى نص مفهوم.
        """
        currency_map = {"1": "ر.ي", "2": "ر.س", "3": "دولار"}
        return currency_map.get(currency_code, "ر.ي")

    def get_all_data(self):
        """
        استرجاع جميع الديون غير المسددة مع المدفوعات المرتبطة بكل دين.
        """
        debts = []
        tables = [("Passports", "booking_date")]

        for table, date_column in tables:
            records = self.db_manager.select_with_condition(table, "remaining_amount > 0")

            for record in records:
                payments = self.get_payments(table, record[0])
                debt_data = self.get_passport_data(record)
                # إضافة قائمة المدفوعات (إذا كانت موجودة)
                debt_data["payments"] = [
                    {
                        "amount": payment[3],
                        "date": payment[4],
                        "method": payment[5]
                    }
                    for payment in payments
                ]

                debts.append(debt_data)

        # فرز الديون بناءً على التاريخ (إن وجد)
        debts.sort(
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d") if x["date"] else datetime.min,
            reverse=True
        )
        
        return debts

    def get_passport_data(self, record):
        return {
            "id": record[0],
            "name": record[1],
            "type": "passport",
            "date": record[2],
            "ym_paid": record[4] if record[-1] == '1' else 0 if record[-1] == '3' else 0,
            "sm_paid": record[4] if record[-1] == '2' else 0 if record[-1] == '3' else 0,
            "remaining": record[8],
        }

    def get_by_id(self, debt_id):
        return self.db_manager.select("Passports", id=debt_id)
    def mark_debt_as_paid(self, debt_id, service_type):
        """
        تحديث حالة الدين إلى مدفوع.
        """
        try:
            if service_type == "Passports":
                self.db_manager.update("Passports", debt_id, remaining_amount=0)
            elif service_type == "Umrah":
                self.db_manager.update("Umrah", debt_id, remaining_amount=0)
            elif service_type == "Trips":
                self.db_manager.update("Trips", debt_id, remaining_amount=0)
            return True, "تم تحديث حالة الدين إلى مدفوع."
        except Exception as e:
            return False, f"حدث خطأ أثناء تحديث حالة الدين: {str(e)}"
   

    def export_to_excel(self):
        print("hello wrold")

