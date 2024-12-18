from flask import Flask, render_template, redirect, url_for, request, jsonify, Response
import json
from dbconfig import init_db, db
from models import Toilet
from utils.logger import logger

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gokuhinata1111@localhost/Projects'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

@app.route('/')
def index():
    return '', 200

@app.route('/health')
def health():
    logger.info('Health API')
    return '', 200

@app.route("/login", methods=['POST'])
def login():
    json_data = request.get_json()

    username = json_data['username']
    password = json_data['password']
    
    logger.info('Login: checking username & password')
    if username == "qwe" and password == "qwe":
        response = {
            "success": True,
            "message": "Credentails are valid"
        }
        return response, 200
    else:
        return '', 401

# @app.route("/add_new_toilet", methods=['POST'])
# def add_new_toilet():
#     json_data = request.get_json()
#     print("json_data: ", type(json_data))
#     response = add_toilet(json_data)
#     print("response: ", response)
#     return jsonify(response)

@app.route("/toilet", methods=['POST'])
def add_toilet():
    try:
        toiletData = request.get_json()
        print("json_data: ", type(toiletData))

        existing_toilet = db.session.query(Toilet).filter(
            Toilet.ToiletName == toiletData['ToiletName'],
            Toilet.ToiletAddressLine1 == toiletData['ToiletAddressLine1'],
            Toilet.ToiletCity == toiletData['ToiletCity'],
            Toilet.ToiletState == toiletData['ToiletState']
        ).first()
        
        if existing_toilet:
            print("existing_toilet: ", existing_toilet)
            logger.error("A toilet with the same details already exists")
            logger.info(existing_toilet)
            return {"message": "A toilet with the same details already exists.", "success": False}, 400

        new_toilet = Toilet(**toiletData)
        db.session.add(new_toilet)
        db.session.commit()

        created_toilet = db.session.query(Toilet).filter(
            Toilet.ToiletName == toiletData['ToiletName'],
            Toilet.ToiletAddressLine1 == toiletData['ToiletAddressLine1'],
            Toilet.ToiletCity == toiletData['ToiletCity'],
            Toilet.ToiletState == toiletData['ToiletState']
        ).first()

        return jsonify({"success": True, "message": "Toilet added successfully", "data": { "id": created_toilet.ToiletID }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Failed to add toilet: {str(e)}"}), 400

@app.route("/toilet/all", methods=['GET'])
def get_all_toilets():
    toilets_list = []
    try:
        toilets = Toilet.query.all()  # Fetch all toilet records
        for toilet in toilets:
            toilets_list.append(Toilet.model_to_dict(toilet))
        
        return jsonify({"success": True, "length": len(toilets_list), "data": toilets_list}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to fetch toilets: {str(e)}"}), 404
    
@app.route("/toilet", methods=['GET'])
def get_toilet_by_id():
    try:
        query = request.args.get('id')

        toilet = db.session.query(Toilet).filter_by(ToiletID=query).first()
        
        return jsonify(toilet.model_to_dict())
    except Exception as e:
        print("Exception occured: ", e)
        return '', 404

@app.route("/toilet", methods=['DELETE'])
def delete_toilet_by_id():
    try:
        print("Inside toilet:delete")
        toilet_id = request.args.get('id')
        
        # If no id is provided, return a 400 response
        if toilet_id is None:
            return jsonify({"message": "ID parameter is required"}), 400
        
        # Fetch toilet by ID
        print("Fetching toilet by ID")
        toilet = db.session.query(Toilet).filter_by(ToiletID=toilet_id).first()

        # If toilet not found, return a 404 response
        if toilet is None:
            return '', 404

        # Delete the toilet from the database
        print("Deleting toilet from DB")
        db.session.delete(toilet)
        db.session.commit()

        # Return success message
        return '', 204

    except Exception as e:
        print("Exception occurred: ", e)
        db.session.rollback()
        return jsonify({"success": False, "message": "Something went wrong"}), 400

@app.route("/toilet", methods=['PUT'])
def update_toilet_by_id():
    try:
        print("Inside toilet:update")
        logger.info("Inside toilet:update")
        
        toilet_id = request.args.get('id')
        
        if toilet_id is None:
            logger.error("toilet:update => ID parameter is required")
            return jsonify({"message": "ID parameter is required"}), 400
        
        # Fetching toilet by ID
        print("Fetching toilet by ID")
        logger.info("toilet:update => Fetching toilet by ID")
        toilet = db.session.query(Toilet).filter_by(ToiletID=toilet_id).first()

        # If toilet not found, return a 404 response
        if toilet is None:
            logger.error("toilet:update => toilet not found")
            return '', 404
        
        # Checking request body
        json_data = request.get_json()
        if not json_data:
            logger.error("toilet:update => JSON body is required")
            return jsonify({"message": "JSON body is required"}), 400

        # Check for restricted fields
        restricted_fields = ["ToiletID", "ToiletAddDate"]
        invalid_fields = [field for field in restricted_fields if field in json_data]

        if invalid_fields:
            logger.error(f"toilet:update => Restricted fields attempted: {invalid_fields}")
            return jsonify({
                "message": f"Cannot update restricted fields: {', '.join(invalid_fields)}",
                "success": False
            }), 400

        # Update the toilet info in the database
        print("Updating toilet information based on ID")
        logger.info("toilet:update => Updating toilet information based on ID")
        
        # Perform the update query
        update_count = (
            db.session.query(Toilet)
            .filter(Toilet.ToiletID == toilet_id)
            .update(json_data, synchronize_session="fetch")
        )

        if update_count == 0:  # If no rows were updated, it means the toilet ID does not exist
            logger.error("toilet:update => Toilet not found")
            return jsonify({"message": "Toilet not found"}), 404

        db.session.commit()
        # Return success message
        return jsonify({"success": True, "message": "Toilet updated successfully"}), 200

    except Exception as e:
        print("Exception occurred: ", e)
        db.session.rollback()
        logger.error("toilet:update => An exception occurred")
        return jsonify({"success": False, "message": "Something went wrong"}), 400

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=8080, debug=True)