import sqlite3
from typing import List, Dict, Union

class SearchManager:
    def __init__(self, db_name="taif.db"):
        self.db_path = f"database/{db_name}"
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def search(self, table_name: str, columns: List[str], search_term: str, exact_match: bool = False) -> List[Dict[str, Union[str, float, int]]]:
        """
        بحث في جدول معين باستخدام عمود أو أكثر.

        :param table_name: اسم الجدول المراد البحث فيه.
        :param columns: قائمة بالأعمدة المراد البحث فيها.
        :param search_term: النص المراد البحث عنه.
        :return: قائمة بالصفوف التي تطابق البحث.
        """
        if not columns:
            raise ValueError("يجب تحديد عمود واحد على الأقل للبحث.")

        # بناء الاستعلام الديناميكي
        conditions = " OR ".join([f"{column} LIKE ?" for column in columns])
        query = f"SELECT * FROM {table_name} WHERE {conditions}"
        
        # إضافة علامة % للبحث الجزئي
        search_term = f"%{search_term}%"
        params = [search_term] * len(columns)

        # تنفيذ الاستعلام
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        # تحويل النتائج إلى قائمة من القواميس
        column_names = [description[0] for description in self.cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]

        return results

    def search_multiple_tables(self, tables: List[str], columns: List[str], search_term: str) -> List[Dict[str, Union[str, float, int]]]:
        """
        بحث في أكثر من جدول باستخدام عمود أو أكثر.

        :param tables: قائمة بجداول البحث.
        :param columns: قائمة بالأعمدة المراد البحث فيها.
        :param search_term: النص المراد البحث عنه.
        :return: قائمة بالصفوف التي تطابق البحث من جميع الجداول.
        """
        results = []
        for table in tables:
            table_results = self.search(table, columns, search_term)
            results.extend(table_results)
        return results

    def search_debts(self, search_term: str, exact_match: bool = False) -> List[Dict[str, Union[str, float, int]]]:
        """
        بحث في جداول الديون (Passports, Umrah, Trips) باستخدام مصطلح البحث.

        :param search_term: النص المراد البحث عنه.
        :return: قائمة بالصفوف التي تطابق البحث بنفس تنسيق get_all_data.
        """
        search_tables = [
            ("Passports", ["name", "receiver_name", "status", "type"]),
            ("Umrah", ["name", "passport_number", "phone_number", "sponsor_number", "sponsor_name"]),
            ("Trips", ["name", "passport_number", "from_place", "to_place", "booking_company", "amount"])
        ]

        results = []
        for table, columns in search_tables:
            try:
                # البحث في الجدول
                records = self.search(table, columns, search_term, exact_match)
                for record in records:
                    # تحويل النتيجة إلى تنسيق متوافق مع get_all_data
                    formatted_data = self.format_debt_record(table, record)
                    results.append(formatted_data)
            except Exception as e:
                print(f"Error searching in table {table}: {e}")
                continue

        return results

    def format_debt_record(self, table: str, record: Dict[str, Union[str, float, int]]) -> Dict[str, Union[str, float, int]]:
        """
        تنسيق سجل الدين ليصبح متوافقًا مع تنسيق get_all_data.

        :param table: اسم الجدول (Passports, Umrah, Trips).
        :param record: السجل الذي تم استرجاعه من البحث.
        :return: سجل منسق.
        """
        if table == "Passports":
            return {
                "id": record.get("id", ""),
                "name": record.get("name", ""),
                "type": "Passports",
                "date": record.get("booking_date", ""),
                "ym_paid": f"{record.get('booking_price', 0)} ر.ي" if record.get('currency') == '1' else "0",
                "sm_paid": f"{record.get('booking_price', 0)} ر.س" if record.get('currency') == '2' else "0",
                "remaining": record.get("remaining_amount", 0),
            }
        elif table == "Umrah":
            return {
                "id": record.get("id", ""),
                "name": record.get("name", ""),
                "type": "Umrah",
                "date": record.get("entry_date", ""),
                "ym_paid": f"{record.get('cost', 0)} ر.ي" if record.get('currency') == '1' else "0",
                "sm_paid": f"{record.get('cost', 0)} ر.س" if record.get('currency') == '2' else "0",
                "remaining": record.get("remaining_amount", 0),
            }
        elif table == "Trips":
            return {
                "id": record.get("id", ""),
                "name": record.get("name", ""),
                "type": "Trips",
                "date": record.get("trip_date", ""),
                "ym_paid": f"{record.get('amount', 0)} ر.ي" if record.get('currency') == '1' else "0",
                "sm_paid": f"{record.get('amount', 0)} ر.س" if record.get('currency') == '2' else "0",
                "remaining": record.get("remaining_amount", 0),
            }
        else:
            raise ValueError(f"جدول غير معروف: {table}")
            
    def close(self):
        """إغلاق الاتصال بقاعدة البيانات."""
        self.connection.close()