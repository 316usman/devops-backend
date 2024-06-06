from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
DB_USERNAME = os.environ.get('DB_USERNAME', 'default_username')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_password')
DB_HOST = os.environ.get('DB_HOST', 'default_host')
DB_NAME = os.environ.get('DB_NAME', 'default_dbname')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input1 = db.Column(db.String(100), nullable=False)
    input2 = db.Column(db.String(100), nullable=False)
    input3 = db.Column(db.String(100), nullable=True)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    input1 = data.get('input1')
    input2 = data.get('input2')
    input3 = data.get('input3')

    if not input1 or not input2:
        return jsonify({"error": "input1 and input2 are required"}), 400

    new_data = Data(input1=input1, input2=input2, input3=input3)
    db.session.add(new_data)
    db.session.commit()

    return jsonify({"message": "Data saved successfully"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=4000)
