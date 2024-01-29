from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Reshwanth123$@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Zoho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_source = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    
    def __init__(self,id,lead_source,first_name,last_name,email,phone):
        self.id = id
        self.lead_source = lead_source
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    




# Zoho CRM API credentials
ZOHO_API_ENDPOINT = "https://www.zohoapis.com/crm/v2/"
ZOHO_MODULE_API_NAME = "Leads"
ZOHO_AUTH_TOKEN = "1000.3c4c538948fc7adaec6919c82b33decf.2fb70056700916b7faee35065ea9b321"

r = requests.post("https://accounts.zoho.com/oauth/v2/token?refresh_token=1000.99f7e2710d56f579035a0abe6feb8f9d.23b29426d7bc5adbcfbec7b089646d41&client_id=1000.JJMRX7ZYXOYH5GQAQJ9D10JAQALJQT&client_secret=671b057243e0daaf391a6b2721bd47e29ba91dd379&grant_type=refresh_token")
ZOHO_AUTH_TOKEN = r.json().get("access_token")

# Function to fetch Zoho CRM records
def get_zoho_records():
    url = f"{ZOHO_API_ENDPOINT}{ZOHO_MODULE_API_NAME}"
    headers = {
        "Authorization": f"Zoho-oauthtoken {ZOHO_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    # Customize the parameters as needed
    params = {
        # "page": 1,
        # "per_page": 10,
        "criteria": "(First_Name == 'Nagaraj')",
        "fields": "Id,Lead_Source,First_Name,Last_Name,Email,Phone"
        # Add more parameters as needed
    }
    
    print(f"Zoho CRM API Request: {url}?{params}")

    response = requests.get(url, headers=headers, params=params)
    print('Response: ',response)

    if response.status_code == 200:

        data = response.json()
        if data.get("data"):
            for record in data["data"]:
                new_lead = Zoho(
                    id=record.get("Id"),
                    lead_source=record.get("Lead_Source"),
                    first_name=record.get("First_Name"),
                    last_name=record.get("Last_Name"),
                    email=record.get("Email"),
                    phone=record.get("Phone")
                )
                db.session.add(new_lead)

            db.session.commit()
        return data.get("data", [])
        
    else:
        return None
    


# API endpoint to get Zoho CRM records
@app.route("/api/zoho-records")
def api_zoho_records():
    zoho_records = get_zoho_records()
    return zoho_records



if __name__ == "__main__":
    app.run(debug=True)
