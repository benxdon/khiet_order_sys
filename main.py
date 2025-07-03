import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from flask import Flask, request, render_template

#init the data sheet
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)   

sheet_id = "1Mpb3XfInCAJ6lo8mYuD2OvEvhTAaiuFi_iQeB8u8Nn4"
workbook = client.open_by_key(sheet_id)
sheet_name = datetime.now().strftime("%B")


#helper functions
def parse_viet_time(time_str):
    time_str = time_str.lower().strip()
    
    try: 
        parts = time_str.split()
        time_part = parts[0].strip().split("h")
        period = parts[1]
        date_part = parts[2]

        hour = int(time_part[0])
        minute = int(time_part[1]) if len(time_part[1]) > 0 else 0
        day, month = map(int, date_part.split("/"))

        if period in ["chiều", "tối", "đêm"] and hour < 12: 
            hour+=12
        elif period == "trưa" and hour == 12: 
            pass
        elif period == "trưa" and hour < 12: 
            hour+=12 

        year = datetime.now().year
        delivery_dt = datetime(year, month, day, hour, minute)
        return delivery_dt

    except: 
        print("error time parsing")
        return None


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
                    "item": parts[0].capitalize(),
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
            delivery_dt = parse_viet_time(delivery_time)
        elif "Giảm giá" in line: 
            discount = line.split(":",1)[1].strip()
        elif "Freebies" in line:
            freebies = line.split(":", 1)[1].strip()
        elif "Phương thức" in line: 
            method = line.split(":", 1)[1].strip()
        elif "Ghi chú" in line: 
            notes = line.split(":", 1)[1].strip()
    if delivery_dt is None:
        delivery_dt = datetime.now()

    #parsing data to gg sheet

    for cake in cakes_info:
        row = [
            "", #Xong
            delivery_dt.strftime("%Y-%m-%d"),
            name,
            "", #IG
            phone,
            cake["item"],
            "Có" if cake["topping"] == True else "Không",
            cake["qty"],
            "", #giá lẻ
            discount,
            freebies, 
            "", #tổng
            address,
            notes
        ]
        try:
            print(insert_index)
            sheet.update(f"A{insert_index}:N{insert_index}", [row])
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