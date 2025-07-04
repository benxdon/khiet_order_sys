import gspread
from datetime import datetime
import os, json
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template

#init the data sheet
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
service_account_info = json.loads(os.environ["google_creds"])
creds = Credentials.from_service_account_info(service_account_info,scopes=scopes)
client = gspread.authorize(creds)   

sheet_id = "1Mpb3XfInCAJ6lo8mYuD2OvEvhTAaiuFi_iQeB8u8Nn4"
workbook = client.open_by_key(sheet_id)
sheet_name = datetime.now().strftime("%B")


#helper functions
def total_calc(type, topping, discount, qty): 
    prices = {"custard": 55000, "mango n cheese": 80000, "meat floss": 65000, "matcha": 50000}
    base = prices[type]
    if topping:
        base += 10000
    total = base * qty * (1 - discount * 0.01)
    return round(total) 


#init the web page
app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
    return render_template("form.html")

#interpreting the data given
@app.route("/submit", methods=["POST"])
def submit():
    try : 
        sheet = workbook.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        template = workbook.worksheet("template")
        sheet = template.duplicate(new_sheet_name=sheet_name)
    vals = sheet.col_values(3)
    insert_index = len(vals) + 1
    order_text = request.form.get("order_text")
    name = phone = address = deli_date = freebies = notes = IG = ""
    discount = 0
    prices = {"custard": 55000, "mango n cheese": 80000, "meat floss": 65000, "matcha": 50000}

    
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
                        "item": stuff[0].strip().lower(),
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
                    "item": parts[0].strip().lower(),
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
            parts = delivery_time.split()
            date, month = parts[2].split("/") 
            time = parts[0] + " " + parts[1]
            year = datetime.now().year
            deli_date = datetime(year, int(month), int(date)).date()
        elif "Giảm giá" in line: 
            discount = line.split(":",1)[1].strip()
        elif "Freebies" in line:
            freebies = line.split(":", 1)[1].strip()
        elif "Ghi chú" in line: 
            notes = line.split(":", 1)[1].strip()
        elif "IG" in line:
            IG = line.split(":",1)[1].strip()
    if deli_date is None:
        deli_date = datetime.now().date()

    #parsing data to gg sheet
    for cake in cakes_info:
        row = [
            "", #Xong
            deli_date.strftime("%d/%m/%y"),
            name,
            IG, #IG
            phone,
            cake["item"],
            "Có" if cake["topping"] == True else "Không",
            cake["qty"],
            prices[cake["item"]], #giá lẻ
            discount,
            freebies, 
            total_calc(cake["item"], cake["topping"], int(discount), cake["qty"]), #tổng
            address,
            time,
            notes,
            None #method
        ]
        try:
            sheet.update(f"A{insert_index}:P{insert_index}", [row])
            insert_index+=1
        except Exception as e: 
            print("error appending row:", e)
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
'''