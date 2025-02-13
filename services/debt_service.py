from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from datetime import datetime

class DebtService:
    def __init__(self, master):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
    
    def get_payments(self, debt_type, debt_id):
        """
        استرجاع جميع المدفوعات المرتبطة بدين معين.
        """
        return self.db_manager.select("Payments",
            debt_type=debt_type,
            debt_id=debt_id
        )
    

    def get_all_data(self):
        """
        استرجاع جميع الديون غير المسددة مع المدفوعات المرتبطة بكل دين.
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
                debt_data = self.format_record_data(table, record)

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

        # فرز الديون بناءً على التاريخ (إذا كانت موجودة وصالحة)
        debts.sort(
            key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d") if isinstance(x["date"], str) and x["date"] else datetime.min,
            reverse=True
        )

        return debts

    def format_record_data(self, table, record):
        if table == "Passports":
            return {
                "id": record[0],
                "name": record[1],
                "type": "Passports",
                "date": record[2] if isinstance(record[2], str) else "",
                "ym_paid": f"{record[4]} ر.ي" if record[-1] == '1' else "0",
                "sm_paid": f"{record[4]} ر.س" if record[-1] == '2' else "0",
                "remaining": record[8],
            }
        elif table == "Umrah":
            return {
                "id": record[0],
                "name": record[1],
                "type": "Umrah",
                "date": record[9] if isinstance(record[9], str) else "",
                "ym_paid": f"{record[6]} ر.ي" if record[-1] == '1' else "0 ",
                "sm_paid": f"{record[6]} ر.س" if record[-1] == '2' else "0 ",
                "remaining": record[7],
            }
        elif table == "Trips":
            return {
                "id": record[0],
                "name": record[1],
                "type": "Trips",
                "date": record[10] if isinstance(record[10], str) else "",
                "ym_paid": f"{record[6]} ر.ي" if record[7] == '1' else "0",
                "sm_paid": f"{record[6]}ر.س" if record[7] == '2' else "0",
                "remaining": record[13],
            }

    def get_by_id(self, debt_id, debt_type):
        if debt_type == "Passports":
            return self.db_manager.select("Passports", id=debt_id)
        elif debt_type == "Umrah":
            return self.db_manager.select("Umrah", id=debt_id)
        elif debt_type == "Trips":
            return self.db_manager.select("Trips", id=debt_id)


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

