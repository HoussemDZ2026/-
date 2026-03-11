from flask import Flask, jsonify, request
from flask_cors import CORS
from brain import FutureSetBrain

app = Flask(__name__)
CORS(app) # باش تقدر تربط الموقع مع الـ Frontend لاحقاً

# تشغيل العقل مرة واحدة عند إقلاع السيرفر
try:
    brain_logic = FutureSetBrain()
except Exception as e:
    brain_logic = None

@app.route('/')
def home():
    return "<h1>Future Set Server is LIVE!</h1><p>السيرفر شغال بنجاح يا حسام، جرب مسار /run</p>"

@app.route('/run')
def run():
    if not brain_logic:
        return jsonify({"status": "error", "message": "Brain not initialized"}), 500
        
    user_msg = request.args.get('msg', 'مرحبا')
    try:
        response = brain_logic.get_response(user_msg)
        return jsonify({
            "status": "success",
            "reply": response
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
