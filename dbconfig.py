from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

def init_db(app):
    # Associate the app with the SQLAlchemy instance
    db.init_app(app)
    with app.app_context():
        db.create_all()

"""
# Route to handle adding a new toilet
@app.route("/add-new-toilet", methods=['POST'])
def add_new_toilet():
    json_data = request.get_json()  # Parse incoming JSON data
    response = add_toilet(json_data)
    return jsonify(response)  # Return response as JSON

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
"""