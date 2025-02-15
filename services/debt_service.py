from database.database_manager import DatabaseManager
from database.SearchManager import SearchManager
from datetime import datetime
from reports.debt_exporter import DebtExporter
import tkinter as tk

class DebtService:
    def __init__(self, master):
        self.db_manager = DatabaseManager()
        self.search_manager = SearchManager()
        self.master = master
    
    
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
                debt_data = self.format_record_data(table, record)
                debts.append(debt_data)

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
                "remaining": record[8],
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
        export_screen = DebtExporter(self.master, self)


    def get_payments(self, debt_type, debt_id):
        """استرجاع المدفوعات مع التنسيق الجديد"""
        payments = self.db_manager.select("Payments",
            debt_type=debt_type,
            debt_id=debt_id
        )
        return [{
            "id": p[0],
            "amount": p[3],
            "payment_date": p[4],
            "payment_method": p[5]
        } for p in payments]
    
    def add_payment(self, debt_type, debt_id, amount, payment_date, payment_method):
        """إضافة عملية دفع جديدة وتحديث المبالغ"""
        try:
            self.db_manager.connection.execute("BEGIN TRANSACTION")
            
            # 1. إضافة الدفعة الجديدة
            self.db_manager.insert("Payments", **{
                "debt_type": debt_type,
                "debt_id": debt_id,
                "amount": amount,
                "payment_date": payment_date,
                "payment_method": payment_method,
            })

            # 2. تحديث الجدول الرئيسي
            table_indexes = {
                "Passports": {
                    "price_col": 4,  # booking_price
                    "paid_col": 7,   # paid_amount
                    "remaining_col": 8  # remaining_amount
                },
                "Umrah": {
                    "price_col": 6,  # cost
                    "paid_col": 7,   # paid
                    "remaining_col": 8  # remaining_amount
                },
                "Trips": {
                    "price_col": 6,  # amount
                    "paid_col": 12,  # paid
                    "remaining_col": 13  # remaining_amount
                }
            }

            # الحصول على البيانات الحالية
            current_data = self.db_manager.select(debt_type, id=debt_id)[0]
            price_idx = table_indexes[debt_type]["price_col"]
            paid_idx = table_indexes[debt_type]["paid_col"]

            total_price = current_data[price_idx]
            current_paid = current_data[paid_idx]

            # حساب القيم الجديدة
            new_paid = float(current_paid) + float(amount)
            new_remaining = float(total_price) - float(new_paid)
            print(f"new_paid {new_paid}")
            print(f"new_remaining {new_remaining}")

            # تحديث الأعمدة باستخدام الفهرس
            success, message = self.db_manager.update_by_index(
                table_name=debt_type,
                identifier=debt_id,
                column_indexes=[
                    table_indexes[debt_type]["paid_col"],  # فهرس العمود المدفوع
                    table_indexes[debt_type]["remaining_col"]  # فهرس العمود المتبقي
                ],
                new_values=[new_paid, new_remaining]
            )

            if not success:
                raise Exception(message)

            self.db_manager.connection.commit()
            return True, "تمت إضافة الدفعة وتحديث الحسابات بنجاح"

        except Exception as e:
            self.db_manager.connection.rollback()
            return False, f"فشلت العملية: {str(e)}"
        
#