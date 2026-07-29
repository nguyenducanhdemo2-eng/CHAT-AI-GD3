import os
from flask import Flask, render_template, request, jsonify
import google.genai as genai

app = Flask(__name__)

# ĐIỀN API KEY VÀO ĐÂY HOẶC SỬ DỤNG BIẾN MÔI TRƯỜNG
API_KEY = os.environ.get("API_KEY", "AQ.Ab8RN6JlPDSqHTFv9kIeiVzV8CWgfxr6kCRmv17yqZfRtaCsCA")
if not API_KEY:
    raise ValueError("Thiếu API_KEY. Thiết lập biến môi trường API_KEY hoặc gán trực tiếp vào app.py")

client = genai.Client(api_key=API_KEY)

# KHAI BÁO MODEL
MODEL_ID = "models/gemini-flash-lite-latest"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Tin nhắn không được để trống"}), 400

        # Gọi API với model chuẩn
        response = client.models.generate_content(model=MODEL_ID, contents=user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        # Ghi log lỗi chi tiết ra cửa sổ Terminal để dễ kiểm tra
        error_message = str(e)
        print("\n[LOI API]:", error_message, "\n")
        if "RESOURCE_EXHAUSTED" in error_message or "Quota exceeded" in error_message:
            error_message = "Bạn đã vượt quá hạn mức API. Hãy kiểm tra kế hoạch/billing hoặc đổi API key khác."
        return jsonify({"error": error_message}), 500

if __name__ == "__main__":
    # Để port=5050 để tránh trùng lặp cổng nếu port 5000 đang bị kẹt
    app.run(debug=True, port=5050)