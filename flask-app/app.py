from flask import Flask, request, jsonify, render_template
from backend_scraper import get_attendance_summary_selenium
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super-secret-dev-key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_attendance', methods=['POST'])
def get_attendance():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    print(f"Received request for attendance for user: {username}")
    attendance_results = get_attendance_summary_selenium(username, password)
    print(f"Selenium finished for {username}. Success: {attendance_results['success']}")

    return jsonify(attendance_results)

if __name__ == '__main__':
    # Don't use app.run in production on Render. Use gunicorn.
    app.run(host="0.0.0.0", port=5000)
