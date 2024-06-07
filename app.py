from flask import Flask, request, jsonify
import pymysql
import os
from dotenv import load_dotenv

app = Flask(__name__)


# Load environment variables from .env file
load_dotenv()

# Configuration
DB_USERNAME = os.getenv('DB_USERNAME', 'default_username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_HOST = os.getenv('DB_HOST', 'default_host')
DB_NAME = os.getenv('DB_NAME', 'default_dbname')

# Connect to the database
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=3306
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Route to add data
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    input1 = data.get('input1')
    input2 = data.get('input2')
    input3 = data.get('input3')

    if not input1 or not input2:
        return jsonify({"error": "input1 and input2 are required"}), 400

    try:
        # Execute the SQL query to insert data into the database
        query = "INSERT INTO data (input1, input2, input3) VALUES (%s, %s, %s)"
        cursor.execute(query, (input1, input2, input3))
        connection.commit()
        return jsonify({"message": "Data added successfully"}), 201
    except Exception as e:
        # If an error occurs, rollback the transaction and return an error response
        connection.rollback()
        return jsonify({"error": f"Failed to add data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
