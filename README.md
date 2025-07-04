# khiet_order_sys
# 🥐 Khiet Order Automation
Hi everyone, this is an application built using flask, html and render to help my friend's small business in selling croissants. I noticed that she typed everything manually on to the Google Sheets after the customers send her the text messages on IG so I thought of building an web application to record the orders straight to the Google Sheets.
# Features
- Easy to use web form for order input
- Automatically send the orders to Google Sheets
- The scripts cleaned and categorize the data
- Calculate total price
- Support schedule delivery time
# Tech Stack
- Backend: Flask (Python)
- Frontend: HTML (Jinja templates)
- Database: Google Sheets (gspread)
- Deployment: Render
# Example input format
template for data entry
`✧ Tên người nhận:
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
✧ Ghi chú: ít ngọt, v.v.`
