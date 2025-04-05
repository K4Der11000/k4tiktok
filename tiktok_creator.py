from flask import Flask, request, render_template_string, send_file, redirect from selenium import webdriver from selenium.webdriver.common.by import By import time import os import sys import random from faker import Faker import pdfkit from datetime import datetime

app = Flask(name) fake = Faker() config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

Admin password for login

ADMIN_PASSWORD = "kader11000"

HTML_FORM = """

<html>
<head><title>TikTok Account Creator</title></head>
<body>
    <h2>Create TikTok Account</h2>
    {% if message %}<p style='color: green;'>{{ message }}</p>{% endif %}
    <form method="post" action="/register">
        <label>Email:</label><br>
        <input type="text" name="email"><br>
        <label>Password:</label><br>
        <input type="text" name="password"><br>
        <label>Username:</label><br>
        <input type="text" name="username"><br>
        <label>Day:</label><br>
        <input type="number" name="day"><br>
        <label>Month:</label><br>
        <input type="number" name="month"><br>
        <label>Year:</label><br>
        <input type="number" name="year"><br><br>
        <input type="submit" value="Register">
    </form><button type="button" onclick="autofill()">Auto Fill Random Data</button>

<form method="post" action="/auto">
    <input type="submit" value="Auto Create One Account">
</form>

<form method="post" action="/auto-multi">
    <label>Number of accounts:</label><br>
    <input type="number" name="count" min="1" max="50" value="5"><br><br>
    <input type="submit" value="Auto Create Multiple Accounts">
</form>

<form method="get" action="/accounts">
    <input type="submit" value="View Saved Accounts">
</form>

<form method="get" action="/download-pdf">
    <input type="submit" value="Download Accounts as PDF">
</form>

<form method="post" action="/restart-script">
    <input type="submit" value="Restart Script">
</form>

<script>
function autofill() {
    document.querySelector('input[name="email"]').value = "user" + Math.floor(Math.random() * 10000) + "@example.com";
    document.querySelector('input[name="password"]').value = Math.random().toString(36).slice(2, 10);
    document.querySelector('input[name="username"]').value = "user" + Math.floor(Math.random() * 100000);
    document.querySelector('input[name="day"]').value = Math.floor(Math.random() * 28 + 1);
    document.querySelector('input[name="month"]').value = Math.floor(Math.random() * 12 + 1);
    document.querySelector('input[name="year"]').value = Math.floor(Math.random() * (2003 - 1985 + 1)) + 1985;
}
</script>

</body>
</html>
"""LOGIN_FORM = """

<html>
<head><title>Login</title></head>
<body>
    <h2>Login</h2>
    <form method="post">
        <label>Password:</label><br>
        <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    {% if error %}<p style='color:red;'>{{ error }}</p>{% endif %}
</body>
</html>
"""def save_account_to_html(email, password, username, day, month, year): file_name = "accounts.html" timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") entry = f""" <tr> <td>{email}</td> <td>{password}</td> <td>{username}</td> <td>{day}/{month}/{year}</td> <td>{timestamp}</td> </tr> """ if not os.path.exists(file_name): with open(file_name, "w", encoding="utf-8") as f: f.write(f""" <html> <head> <title>Saved TikTok Accounts</title> <style> body {{ font-family: Arial; background-color: #f8f9fa; padding: 20px; }} table {{ width: 100%; border-collapse: collapse; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }} th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ccc; }} th {{ background-color: #007bff; color: white; }} tr:hover {{ background-color: #f1f1f1; }} </style> </head> <body> <h2>Accounts Created</h2> <table> <tr><th>Email</th><th>Password</th><th>Username</th><th>Birthdate</th><th>Timestamp</th></tr> {entry} </table> </body> </html> ") else: with open(file_name, "r+", encoding="utf-8") as f: content = f.read() f.seek(0) f.truncate() content = content.replace("</table>", entry + "</table>") f.write(content)

@app.route("/", methods=["GET", "POST"]) def index(): if request.method == "POST": password = request.form.get("password") if password == ADMIN_PASSWORD: return render_template_string(HTML_FORM) else: return render_template_string(LOGIN_FORM, error="Incorrect password.") return render_template_string(LOGIN_FORM)

@app.route("/register", methods=["POST"]) def register(): email = request.form["email"] password = request.form["password"] username = request.form["username"] day = request.form["day"] month = request.form["month"] year = request.form["year"] save_account_to_html(email, password, username, day, month, year) return render_template_string(HTML_FORM, message="Account saved.")

@app.route("/auto", methods=["POST"]) def auto_create(): email = f"user{random.randint(1000, 9999)}@example.com" password = fake.password(length=8) username = f"user{random.randint(10000, 99999)}" day = random.randint(1, 28) month = random.randint(1, 12) year = random.randint(1985, 2003) save_account_to_html(email, password, username, day, month, year) return render_template_string(HTML_FORM, message=f"Account created automatically: {email}")

@app.route("/auto-multi", methods=["POST"]) def auto_multi(): count = int(request.form.get("count", 1)) success = 0 for _ in range(count): email = f"user{random.randint(1000, 9999)}@example.com" password = fake.password(length=8) username = f"user{random.randint(10000, 99999)}" day = random.randint(1, 28) month = random.randint(1, 12) year = random.randint(1985, 2003) save_account_to_html(email, password, username, day, month, year) success += 1 return render_template_string(HTML_FORM, message=f"{success} of {count} accounts created successfully.")

@app.route("/accounts") def show_accounts(): if os.path.exists("accounts.html"): with open("accounts.html", "r", encoding="utf-8") as f: return f.read() else: return "No saved accounts."

@app.route("/download-pdf") def download_pdf(): html_file = "accounts.html" pdf_file = "accounts.pdf" if not os.path.exists(html_file): return "No saved accounts yet." pdfkit.from_file(html_file, pdf_file, configuration=config) return send_file(pdf_file, as_attachment=True)

@app.route("/restart-script", methods=["POST"]) def restart_script(): python = sys.executable os.execl(python, python, *sys.argv)

if name == "main": app.run(debug=True)

