# khiet_order_sys
# 🥐 Khiet Order Automation

A simple Flask app I built to help my friend Khiet manage bakery orders more efficiently. Instead of manually copying details from DMs, this app parses a structured message and logs it directly to Google Sheets. It also prevents overlapping delivery times.

---

## 📌 Features

- Parse structured order text (name, time, item, etc.)
- Calculate total price (quantity × unit price – discount)
- Support for freebies and custom notes
- Avoid delivery clashes
- Auto-log to a Google Spreadsheet

---

## 📁 Project Structure

```
khiet-order-automation/
├── app.py
├── templates/
│   └── index.html
├── credentials.json
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/khiet-order-automation.git
cd khiet-order-automation
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Google Sheets API
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a service account with Sheets API access
- Download the JSON credentials and rename to `credentials.json`
- Share your target spreadsheet with the service account’s email

---

## 📄 Google Sheet Format

Make sure your Google Sheet has the following columns, in this exact order:

```
Xong | Giờ giao | Tên | IG | SĐT | Loại bánh | Topping | Số lượng | Giá lẻ | Discount | Freebies | Tổng | Địa chỉ | Notes
```

The app will fill each row based on this structure.

---

## ▶️ Running the App

```bash
flask run
```

Then open `http://localhost:5000` in your browser to submit orders.

---

## 🚀 Deployment (optional)

Planning to deploy this to **Render** soon.  
To prepare:

- Add a `Procfile`:
  ```
  web: gunicorn app:app
  ```
- Install `gunicorn`:
  ```bash
  pip install gunicorn
  ```
- Push to GitHub and connect the repo on Render.

---

## 🧠 Notes

- Input must follow the expected format or the parser will break.
- No authentication or security added (for internal use only).
- Future plans: Google Calendar sync, user-friendly UI, conflict resolution.

---

## 📬 Contact

DM me if you’re building something similar or want to tweak this for your own workflow.
