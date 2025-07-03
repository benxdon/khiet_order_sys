import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    order_text = request.form.get("order_text")
    print("Received order text:\n", order_text)
    name = phone = cake_info = address = delivery_time = None
    lines = order_text.splitlines()
    for line in lines: 
        if "Tên người nhận" in line: 
            name = line.split(":", 1)[1].strip()
        elif "Số điện thoại" in line: 
            phone = line.split(":", 1)[1].strip()
        elif "Tên bánh" in line: 
            cake_info = line.split(":", 1)[1].strip()
        elif "Địa chỉ" in line: 
            address = line.split(":", 1)[1].strip()
        elif "Thời điểm" in line: 
            delivery_time = line.split(":", 1)[1].strip()
    order_row = [name, phone, cake_info, address, delivery_time]
    print(order_row)
    return render_template("redir.html")

if __name__ == "__main__":
    app.run(debug=True)

'''
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1Mpb3XfInCAJ6lo8mYuD2OvEvhTAaiuFi_iQeB8u8Nn4"
workbook = client.open_by_key(sheet_id)

sheets = workbook.worksheets()
print(sheets)
'''