import os
from flask import Flask, jsonify, request
from brain import FutureSetBrain
from tools import FutureSetTools
from auth import FutureSetAuth
from dotenv import load_dotenv

load_dotenv()

# إعداد Flask
app = Flask(__name__)

class FutureSetApp:
    def __init__(self):
        self.brain = FutureSetBrain()
        self.tools = FutureSetTools()
        self.auth = FutureSetAuth()

    def run_app(self, user_email, user_message):
        is_active, message = self.auth.check_subscription(user_email)
        if not is_active:
            return {"status": "error", "message": message}

        ai_response = self.brain.get_response(user_message)
        final_output = ai_response
        
        if "صورة" in user_message or "تصميم" in user_message:
            image_url = self.tools.generate_image_ad(ai_response)
            final_output = f"{ai_response}\n\n🔗 رابط التصميم: {image_url}"

        final_output = self.tools.format_for_facebook(final_output)
        return {"status": "success", "data": final_output}

# إنشاء نسخة من التطبيق
fs_logic = FutureSetApp()

# الصفحة الرئيسية للموقع
@app.route('/')
def home():
    return "<h1>مرحباً بك في منصة فيوتر سيت (Future Set)</h1><p>السيرفر يعمل بنجاح!</p>"

# رابط (API) لاستقبال الطلبات
@app.route('/run', methods=['GET'])
def run():
    email = request.args.get('email', 'test@gmail.com')
    msg = request.args.get('msg', 'سلام')
    result = fs_logic.run_app(email, msg)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
