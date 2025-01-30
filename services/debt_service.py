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
        استرجاع جميع الديون غير المسددة.
        """
        debts = []
        tables = [
            ("Passports", "booking_date"),
            ("Umrah", "entry_date"),
            ("Trips", "trip_date")
        ]
        
        for table, date_column in tables:
            records = self.db_manager.select_with_condition(table, "remaining_amount > 0")
            for record in records:
                payments = self.get_payments(table, record[0])
                debt_data = {
                    "id": record[0],
                    "name": record[1],
                    "type": table,
                    "date": record[2] if table == "Passports" else record[9] if table == "Umrah" else record[10],  # التاريخ المناسب
                    "total": record[6],  # net_amount
                    "paid": record[7],   # paid_amount
                    "remaining": record[8], # remaining_amount
                    "currency": self.format_currency(record[-1]),
                    "payments": []
                }
                
                for idx, payment in enumerate(payments, 1):
                    debt_data["payments"].append({
                        "number": idx,
                        "amount": payment[3],
                        "date": payment[4],
                        "method": payment[5]
                    })
                
                debts.append(debt_data)
        
        debts.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d") if x["date"] else datetime.min, reverse=True)
        
        return [list(debt.values()) for debt in debts]

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

