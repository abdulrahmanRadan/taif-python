# login_screen.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
from database.database_manager import DatabaseManager

# إعدادات التنسيق العامة
BG_COLOR = "#f0f0f0"
BUTTON_STYLES = {
    "login": {"bg": "#4CAF50", "active": "#45a049"},
    "create": {"bg": "#2196F3", "active": "#1976D2"},
    "back": {"bg": "#607D8B", "active": "#455A64"},
    "save": {"bg": "#FF9800", "active": "#F57C00"}
}
ENTRY_STYLE = {
    "borderwidth": 2,
    "relief": "flat",
    "highlightbackground": "#CCCCCC",
    "highlightthickness": 1,
    "font": ("Arial", 10)
}
LABEL_STYLE = {
    "bg": BG_COLOR,
    "fg": "#333333",
    "font": ("Arial", 10)
}

class LoginScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("تسجيل الدخول")
        self.geometry("350x350")
        self.configure(bg=BG_COLOR)
        self.master = master
        
        # وضع النافذة في منتصف الشاشة
        self.center_window()
        
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def center_window(self):
        """يضع النافذة في منتصف الشاشة"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        # الحاوية الرئيسية
        self.main_frame = tk.Frame(self, bg=BG_COLOR)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # إنشاء الإطارات
        self.login_frame = self.create_login_frame()
        self.create_user_frame = self.create_user_form()
        
        self.show_login_frame()

    def create_login_frame(self):
        frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        
        # اسم المستخدم
        tk.Label(frame, text="اسم المستخدم:", **LABEL_STYLE).pack(pady=5)
        self.username_entry = tk.Entry(frame, **ENTRY_STYLE)
        self.username_entry.pack(pady=5)
        
        # كلمة المرور
        tk.Label(frame, text="كلمة المرور:", **LABEL_STYLE).pack(pady=5)
        self.password_entry = tk.Entry(frame, show="*", **ENTRY_STYLE)
        self.password_entry.pack(pady=5)
        
        # أزرار التحكم
        button_frame = tk.Frame(frame, bg=BG_COLOR)
        button_frame.pack(pady=15)
        
        self.create_button(button_frame, "تسجيل الدخول", "login", self.login).pack(side=tk.RIGHT, padx=5)
        self.create_button(button_frame, "إنشاء حساب", "create", self.show_create_frame).pack(side=tk.LEFT, padx=5)
        
        return frame

    def create_user_form(self):
        frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        
        # الحقول الجديدة
        fields = [
            ("اسم المستخدم الجديد:", "new_username"),
            ("كلمة المرور:", "new_password"),
            ("تأكيد كلمة المرور:", "confirm_password")
        ]
        
        for text, var_name in fields:
            tk.Label(frame, text=text, **LABEL_STYLE).pack(pady=5)
            entry = tk.Entry(frame, show="*" if "password" in var_name else "", **ENTRY_STYLE)
            setattr(self, f"{var_name}_entry", entry)
            entry.pack(pady=5)
        
        # أزرار التحكم
        button_frame = tk.Frame(frame, bg=BG_COLOR)
        button_frame.pack(pady=15)
        
        self.create_button(button_frame, "حفظ", "save", self.save_user).pack(side=tk.RIGHT, padx=5)
        self.create_button(button_frame, "رجوع", "back", self.show_login_frame).pack(side=tk.LEFT, padx=5)
        
        return frame

    def create_button(self, parent, text, style_type, command):
        style = BUTTON_STYLES[style_type]
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=style["bg"],
            fg="white",
            activebackground=style["active"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            borderwidth=0,
            relief="flat"
        )

    def show_login_frame(self):
        self.create_user_frame.pack_forget()
        self.login_frame.pack(expand=True)
        
    def show_create_frame(self):
        self.login_frame.pack_forget()
        self.create_user_frame.pack(expand=True)

    def validate_fields(self, fields):
        """يتحقق من أن الحقول ليست فارغة"""
        for field, value in fields.items():
            if not value.strip():
                messagebox.showerror("خطأ", f"يرجى ملء حقل '{field}'")
                return False
        return True

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # التحقق من الحقول الفارغة
        if not self.validate_fields({"اسم المستخدم": username, "كلمة المرور": password}):
            return
            
        db = DatabaseManager()
        user_exists = db.exists("Users", username=username, password=password)
        db.close()
        
        if user_exists:
            self.destroy()
            self.master.deiconify()
        else:
            messagebox.showerror("خطأ", "بيانات الدخول غير صحيحة!")

    def save_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm = self.confirm_password_entry.get()
        
        # التحقق من الحقول الفارغة
        if not self.validate_fields({
            "اسم المستخدم الجديد": username,
            "كلمة المرور": password,
            "تأكيد كلمة المرور": confirm
        }):
            return
            
        if password != confirm:
            messagebox.showerror("خطأ", "كلمات المرور غير متطابقة!")
            return
            
        db = DatabaseManager()
        try:
            db.insert("Users", username=username, password=password)
            messagebox.showinfo("نجاح", "تم إنشاء الحساب بنجاح!")
            self.show_login_frame()
        except sqlite3.IntegrityError:
            messagebox.showerror("خطأ", "اسم المستخدم موجود مسبقاً!")
        finally:
            db.close()

    def on_close(self):
        self.master.destroy()