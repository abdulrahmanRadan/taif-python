class Validator:
    def __init__(self):
        self.errors = {}  # لتخزين الأخطاء لكل حقل

    def validate(self, data, rules):
        """
        يقوم بالتحقق من البيانات بناءً على القواعد المحددة.
        :param data: البيانات المراد التحقق منها (قاموس).
        :param rules: القواعد لكل حقل (قاموس).
        :return: True إذا كانت البيانات صحيحة، False إذا كانت هناك أخطاء.
        """
        self.errors = {}  # إعادة تهيئة قائمة الأخطاء
        is_valid = True

        for field, field_rules in rules.items():
            if field not in data:
                self.errors[field] = ["الحقل غير موجود."]
                is_valid = False
                continue

            value = data[field]
            field_errors = []

            for rule in field_rules:
                if ":" in rule:
                    rule_name, rule_value = rule.split(":")
                    rule_value = rule_value.strip()
                else:
                    rule_name = rule
                    rule_value = None

                # استدعاء الدالة المناسبة بناءً على اسم القاعدة
                if hasattr(self, f"rule_{rule_name}"):
                    error = getattr(self, f"rule_{rule_name}")(value, rule_value)
                    if error:
                        field_errors.append(error)
                else:
                    raise ValueError(f"Unknown validation rule: {rule_name}")

            if field_errors:
                self.errors[field] = field_errors
                is_valid = False

        return is_valid

    def get_errors(self):
        """إرجاع الأخطاء."""
        return self.errors

    def rule_required(self, value, _):
        """التحقق من أن الحقل مطلوب."""
        if not value or (isinstance(value, str) and value.strip() == ""):
            return "هذا الحقل مطلوب."
        return None

    def rule_min(self, value, min_value):
        """التحقق من أن القيمة أكبر من أو تساوي الحد الأدنى."""
        if isinstance(value, (int, float)):
            if value < float(min_value):
                return f"يجب أن تكون القيمة أكبر من أو تساوي {min_value}."
        elif isinstance(value, str):
            if len(value) < int(min_value):
                return f"يجب أن يكون طول النص على الأقل {min_value} حرفًا."
        return None

    def rule_max(self, value, max_value):
        """التحقق من أن القيمة أقل من أو تساوي الحد الأقصى."""
        if isinstance(value, (int, float)):
            if value > float(max_value):
                return f"يجب أن تكون القيمة أقل من أو تساوي {max_value}."
        elif isinstance(value, str):
            if len(value) > int(max_value):
                return f"يجب أن يكون طول النص على الأكثر {max_value} حرفًا."
        return None

    def rule_numeric(self, value, _):
        """التحقق من أن القيمة رقمية."""
        if not isinstance(value, (int, float)):
            return "يجب أن تكون القيمة رقمية."
        return None

    def rule_string(self, value, _):
        """التحقق من أن القيمة نصية."""
        if not isinstance(value, str):
            return "يجب أن تكون القيمة نصية."
        return None

    def rule_email(self, value, _):
        """التحقق من أن القيمة بريد إلكتروني صحيح."""
        if "@" not in value or "." not in value:
            return "يجب أن تكون القيمة بريدًا إلكترونيًا صحيحًا."
        return None

    def rule_phone(self, value, _):
        """التحقق من أن القيمة رقم هاتف صحيح."""
        if not value.isdigit() or len(value) != 9:
            return "يجب أن تكون القيمة رقم هاتف صحيح"
        return None