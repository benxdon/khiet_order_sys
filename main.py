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