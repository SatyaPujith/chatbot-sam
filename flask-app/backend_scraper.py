from playwright.sync_api import sync_playwright
import os

def get_attendance_summary_playwright(username, password):
    result = {
        "present": 0,
        "absent": 0,
        "percentage": 0.0,
        "message": "Failed to retrieve attendance.",
        "success": False
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://samvidha.iare.ac.in/")

            page.fill('#txt_uname', username)
            page.fill('#txt_pwd', password)
            page.click('#but_submit')

            page.wait_for_timeout(3000)

            # Check login success
            if "login" in page.url or "invalid" in page.content().lower():
                result["message"] = "Login failed. Please check your credentials."
                return result

            page.goto("https://samvidha.iare.ac.in/home?action=course_content")
            page.wait_for_timeout(5000)

            text = page.content().upper()
            present = text.count("PRESENT")
            absent = text.count("ABSENT")
            total = present + absent

            result["present"] = present
            result["absent"] = absent
            if total > 0:
                result["percentage"] = round((present / total) * 100, 2)
            result["message"] = "Attendance retrieved successfully."
            result["success"] = True
            browser.close()

    except Exception as e:
        result["message"] = f"Error: {str(e)}"
        result["success"] = False

    return result
