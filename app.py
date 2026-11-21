import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder=".", static_url_path="")

WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL",
    "https://discord.com/api/webhooks/1573352278713303052/1CJuJ0LpyAKOAxxLRhz_gMqrCbmtBc2p5Vvcakur5_cW4l7dLKd3aWjJOqwlzPuzUgwz",
)


@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")


@app.route("/api/webhook", methods=["POST"])
def forward_webhook():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "إشعار جديد من Earn Robox")).strip()
    fields = data.get("fields", [])
    color = data.get("color", 0x00F0FF)

    safe_fields = []
    if isinstance(fields, list):
        for item in fields[:15]:
            if isinstance(item, dict):
                name = str(item.get("name", "")).strip()[:256]
                value = str(item.get("value", "")).strip()[:1024]
                inline = bool(item.get("inline", False))
                if name and value:
                    safe_fields.append({"name": name, "value": value, "inline": inline})

    payload = {
        "embeds": [
            {
                "title": title[:256],
                "color": int(color) if isinstance(color, (int, float)) else 0x00F0FF,
                "fields": safe_fields,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]
    }

    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if 200 <= resp.status_code < 300:
            return jsonify({"ok": True}), 200
        return jsonify({"ok": False, "discord_status": resp.status_code}), 502
    except requests.RequestException as exc:
        return jsonify({"ok": False, "error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
