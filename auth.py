import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class FutureSetAuth:
    def __init__(self):
        # كلمة السر الخاصة بك كمدير (موجودة في .env)
        self.admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        # قاعدة بيانات بسيطة (في الواقع يفضل استخدام Firebase أو JSON)
        # هنا سنضع تجربة لمستخدم واحد
        self.users_db = {
            "test_user@gmail.com": {
                "expiry_date": "2026-04-01", # تاريخ نهاية الاشتراك
                "is_active": True
            }
        }

    def check_subscription(self, email):
        """التحقق هل المستخدم لا يزال يملك اشتراكاً سارياً"""
        if email not in self.users_db:
            return False, "المستخدم غير موجود."
        
        user = self.users_db[email]
        expiry_date = datetime.strptime(user["expiry_date"], "%Y-%m-%d")
        
        if datetime.now() > expiry_date:
            return False, "انتهت مدة اشتراكك. يرجى التجديد."
        
        return True, "اشتراك ساري المفعول."

    def extend_subscription(self, admin_pass, email, days):
        """وظيفة الرابط السري: تمديد اشتراك المستخدم"""
        if admin_pass != self.admin_password:
            return "خطأ: كلمة سر المدير غير صحيحة!"
        
        if email in self.users_db:
            current_expiry = datetime.strptime(self.users_db[email]["expiry_date"], "%Y-%m-%d")
            new_expiry = current_expiry + timedelta(days=days)
            self.users_db[email]["expiry_date"] = new_expiry.strftime("%Y-%m-%d")
            return f"تم تمديد اشتراك {email} إلى {new_expiry.strftime('%Y-%m-%d')}"
        
        return "المستخدم غير موجود."

# تجربة كود الحماية
if __name__ == "__main__":
    auth = FutureSetAuth()
    # تجربة فحص اشتراك
    status, msg = auth.check_subscription("test_user@gmail.com")
    print(f"حالة الاشتراك: {msg}")
