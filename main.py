import gspread
import time
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    order_text = request.form.get("order_text")
    name = phone = address = delivery_time = freebies = method = notes = ""
    discount = 0.0
    
    #handles cake info
    cakes_info = []
    reading_item = False

    lines = [line.strip() for line in order_text.splitlines() if line.strip()]
    
    for line in lines: 
        if "Tên bánh" in line: 
            parts = line.split(":",1)
            if len(parts) == 2 and "+" in parts[1]:
                item = line.split(":", 1)[1].strip()
                stuff = [x.strip() for x in item.split("+")]
                if len(stuff) == 3: 
                    cakes_info.append({
                        "item": stuff[0].capitalize(),
                        "topping": False if stuff[1].lower() == "ko" else True,
                        "qty": int(stuff[2])
                    })   
            else:
                reading_item = True
            continue
        elif reading_item and line.startswith("✧"):
            reading_item = False
        elif reading_item and line.startswith("-"):
            parts = [x.strip() for x in line[1:].split("+")]
            if len(parts) == 3: 
                cakes_info.append({
                    "cake": parts[0].capitalize(),
                    "topping": False if parts[1].lower() == "ko" else True,
                    "qty": int(parts[2])
                })
    
    #handles other info which is not cake
    for line in lines: 
        if "Tên người nhận" in line: 
            name = line.split(":", 1)[1].strip()
        elif "Số điện thoại" in line: 
            phone = line.split(":", 1)[1].strip() 
        elif "Địa chỉ" in line: 
            address = line.split(":", 1)[1].strip()
        elif "Thời điểm" in line: 
            delivery_time = line.split(":", 1)[1].strip()
        elif "Giảm giá" in line: 
            discount = int(line.split(":",1)[1].strip()) * 0.1
        elif "Freebies" in line:
            freebies = line.split(":", 1)[1].strip()
        elif "Phương thức" in line: 
            method = line.split(":", 1)[1].strip()
        elif "Ghi chú" in line: 
            notes = line.split(":", 1)[1].strip()
    order_row = [name, phone, cakes_info, address, delivery_time, discount, freebies, method, notes]
    print(order_row)

    #parsing data to gg sheet
    return render_template("redir.html")

if __name__ == "__main__":
    app.run(debug=True)

'''
template for data entry
✧ Tên người nhận:
✧ Số điện thoại:
✧ Tên bánh + topping + số lượng:
   - mango + ko + 1
   - blueberry + có + 2
✧ Địa chỉ nhận bánh:
✧ Thời điểm nhận bánh (sau 1 ngày kể từ lúc order):
(nhân viên ghi)
✧ Giảm giá: 10 (không ghi %)
✧ Freebies: (món gì đó)
✧ Phương thức thanh toán: bank/cash
✧ Ghi chú: ít ngọt, v.v.

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