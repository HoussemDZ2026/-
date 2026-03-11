import os
from brain import FutureSetBrain
from tools import FutureSetTools
from auth import FutureSetAuth
from dotenv import load_dotenv

load_dotenv()

class FutureSetApp:
    def __init__(self):
        # استدعاء المكونات الثلاثة
        self.brain = FutureSetBrain()
        self.tools = FutureSetTools()
        self.auth = FutureSetAuth()

    def run_app(self, user_email, user_message):
        print(f"\n--- معالجة طلب للمستخدم: {user_email} ---")
        
        # 1. الخطوة الأولى: التحقق من الاشتراك
        is_active, message = self.auth.check_subscription(user_email)
        if not is_active:
            return {"status": "error", "message": message}

        # 2. الخطوة الثانية: إرسال الطلب لـ "العقل" لتحليله
        ai_response = self.brain.get_response(user_message)

        # 3. الخطوة الثالثة: التحقق هل الطلب يحتاج "أداة" (مثلاً تصميم صورة)
        final_output = ai_response
        
        # منطق بسيط: إذا ذكر العقل كلمة "تصميم" أو "صورة"، نجهز رابط الصورة
        if "صورة" in user_message or "تصميم" in user_message:
            image_url = self.tools.generate_image_ad(ai_response)
            final_output = f"{ai_response}\n\n🔗 رابط التصميم: {image_url}"

        # 4. الخطوة الرابعة: إضافة اللمسة التسويقية (هاشتاغات)
        final_output = self.tools.format_for_facebook(final_output)

        return {"status": "success", "data": final_output}

# تجربة التشغيل الكاملة من الهاتف (Pydroid 3)
if __name__ == "__main__":
    app = FutureSetApp()
    
    # محاكاة مستخدم يطلب إعلاناً
    email = "test_user@gmail.com"
    request = "حاب ندير إعلان صورة لدورة الرياضيات لطلبة الباك"
    
    result = app.run_app(email, request)
    
    if result["status"] == "success":
        print(f"النتيجة النهائية للنشر:\n{result['data']}")
    else:
        print(f"تنبيه: {result['message']}")
