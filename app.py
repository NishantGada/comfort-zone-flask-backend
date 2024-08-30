from flask import Flask, render_template, redirect, url_for, request, jsonify
import json
from dbconfig import init_db, db
from models import Toilet

app = Flask(__name__)

# Configuration for MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gokuhinata1111@localhost/Projects'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    json_data = request.get_json()
    print("json_data: ", type(json_data))

    username = json_data['username']
    password = json_data['password']
    
    print(f"username: {username}, password: {password}")

    if username == "gadanishant" and password == "qweqweqwe":
        data = {
            "success": True,
            "message": "Credentails are Valid"
        }
    else:
        data = {
            "success": False,
            "message": "Credentails are Invalid"
        }
        
    return data

@app.route('/success')
def success():
    return "Form submitted successfully!"

@app.route("/add-new-toilet", methods=['POST'])
def add_new_toilet():
    json_data = request.get_json()  # Parse incoming JSON data
    print("json_data: ", type(json_data))
    # response = add_toilet(json_data)
    # print("response: ", response)
    # return jsonify(response)  # Return response as JSON
    return {}

# Function to add new toilet record
def add_toilet(toiletData):
    try:
        new_toilet = Toilet(**toiletData)
        db.session.add(new_toilet)
        db.session.commit()
        return {"message": "Toilet added successfully!", "success": True}
    except Exception as e:
        db.session.rollback()
        return {"message": f"Failed to add toilet: {str(e)}", "success": False}

if __name__ == '__main__':
    app.run(debug=True)