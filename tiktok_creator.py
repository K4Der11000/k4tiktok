# TikTok Account Creator - Web Interface
# Author: kader11000
# Requirements:
#   pip install flask selenium faker pdfkit
#   Install wkhtmltopdf version 0.12.6 (see below for instructions)

"""
INSTALLING WKHTMLTOPDF 0.12.6 ON ALL SYSTEMS:

1. WINDOWS:
   - Download: https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox-0.12.6-1.msvc2015-win64.exe
   - Install it, then set path in Python:
     config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

2. LINUX (Ubuntu/Debian):
   sudo apt update
   sudo apt install -y xfonts-75dpi xfonts-base libjpeg-turbo8
   wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.buster_amd64.deb
   sudo apt install ./wkhtmltox_0.12.6-1.buster_amd64.deb
   
   config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

3. MACOS:
   brew install --cask wkhtmltopdf
   Or download from:
   https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.6
"""

from flask import Flask, request, render_template_string, send_file, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import sys
import random
from faker import Faker
import pdfkit
from datetime import datetime

app = Flask(__name__)
fake = Faker()
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

ADMIN_PASSWORD = "kader11000"
HTML_FILE = "tiktok_results.html"
results = []

HELP_SECTION = """
<h2>Help & Installation</h2>
<pre style='background:#f5f5f5;padding:10px;border-radius:5px;'>
INSTALLING WKHTMLTOPDF 0.12.6:

1. WINDOWS:
 - Download: https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox-0.12.6-1.msvc2015-win64.exe
 - Install and set path in script:
   config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

2. LINUX (Ubuntu/Debian):
 sudo apt update
 sudo apt install -y xfonts-75dpi xfonts-base libjpeg-turbo8
 wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.buster_amd64.deb
 sudo apt install ./wkhtmltox_0.12.6-1.buster_amd64.deb

3. MACOS:
 brew install --cask wkhtmltopdf
 Or: https://github.com/wkhtmltopdf/wkhtmltopdf/releases/tag/0.12.6
</pre>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form.get("password")
        if password != ADMIN_PASSWORD:
            return "Unauthorized access"
        mode = request.form.get("mode")
        if mode == "auto":
            for _ in range(5):  # example: create 5 accounts
                results.append(create_account())
        return redirect("/")
    return render_template_string(f"""
        <html><body style='font-family:Arial;padding:20px;'>
        <h1>TikTok Account Creator - kader11000</h1>
        <form method="post">
            Password: <input type="password" name="password"><br>
            <button name="mode" value="manual">Create One Account</button>
            <button name="mode" value="auto">Auto Create</button>
        </form><br>
        <a href='/results'>View Results</a> |
        <a href='/download'>Download HTML</a> |
        <a href='/restart'>Restart Script</a> |
        <a href='/help'>Help</a>
        </body></html>
    """)

@app.route("/results")
def view_results():
    table = "<table border='1'><tr><th>Username</th><th>Password</th><th>Date</th></tr>"
    for r in results:
        table += f"<tr><td>{r['username']}</td><td>{r['password']}</td><td>{r['date']}</td></tr>"
    table += "</table>"
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(table)
    return table

@app.route("/download")
def download():
    return send_file(HTML_FILE, as_attachment=True)

@app.route("/restart")
def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)

@app.route("/help")
def help_page():
    return f"""
    <html><head><title>Help - TikTok Creator</title></head>
    <body style='font-family:Arial;padding:20px;'>
    <a href='/'>Back to Home</a>
    {HELP_SECTION}
    </body></html>
    """

def create_account():
    # Fake generation for demo
    username = fake.user_name()
    password = fake.password()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"username": username, "password": password, "date": created_at}

if __name__ == "__main__":
    app.run(debug=True)
