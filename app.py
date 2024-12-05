from flask import Flask, render_template, redirect, url_for, request, jsonify, Response
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
    return '', 200

@app.route('/health')
def health():
    return '', 200

@app.route("/login", methods=['POST'])
def login():
    json_data = request.get_json()

    username = json_data['username']
    password = json_data['password']
    
    if username == "qwe" and password == "qwe":
        response = {
            "success": True,
            "message": "Credentails are valid"
        }
        return response, 200
    else:
        return '', 401

@app.route("/add-new-toilet", methods=['POST'])
def add_new_toilet():
    json_data = request.get_json()  # Parse incoming JSON data
    print("json_data: ", type(json_data))
    response = add_toilet(json_data)
    print("response: ", response)
    return jsonify(response)  # Return response as JSON

@app.route("/get_all_toilets", methods=['GET'])
def get_all_toilets():
    toilets_list = []
    try:
        toilets = Toilet.query.all()  # Fetch all toilet records
        # print("toilets: ", toilets)
        for toilet in toilets:
            toilets_list.append(Toilet.model_to_dict(toilet))
            # print("---------------")
            # print(toilet.__dict__[1:])
        """
        for toilet in toilets:
            toilets_list.append(toilet.__dict__)
        # toilets_list = [toilet.__dict__ for toilet in toilets]  # Convert each record to dict
        print("toilets_list: ", toilets_list)
        """
        return jsonify({"success": True, "length": len(toilets_list), "data": toilets_list}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to fetch toilets: {str(e)}"}), 404

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
    
@app.route("/get_toilet_by_id")
def get_toilet_by_id():
    try:
        query = request.args.get('id')

        toilet = db.session.query(Toilet).filter_by(ToiletID=query).first()
        
        return jsonify(toilet.model_to_dict())
    except Exception as e:
        print("Exception occured: ", e)
        return '', 404


if __name__ == '__main__':
    app.run(debug=True)