import sqlite3
from typing import List, Dict, Union

class SearchManager:
    def __init__(self, db_name="taif.db"):
        self.db_path = f"database/{db_name}"
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def search(self, table_name: str, columns: List[str], search_term: str) -> List[Dict[str, Union[str, float, int]]]:
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

    def close(self):
        """إغلاق الاتصال بقاعدة البيانات."""
        self.connection.close()