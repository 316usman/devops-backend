from flask import Flask, request, jsonify
import pymysql
import os
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, origins=['http://10.0.4.101', 'http://10.0.5.211'])

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


create_table_query = """
CREATE TABLE IF NOT EXISTS data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input1 VARCHAR(255) NOT NULL,
    input2 VARCHAR(255) NOT NULL,
    input3 VARCHAR(255)
);
"""
cursor.execute(create_table_query)

try:
    # Execute the SQL query to create the table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'data' created successfully or already exists.")
except Exception as e:
    # If an error occurs, rollback the transaction and print an error message
    connection.rollback()
    print(f"Failed to create table 'data': {str(e)}")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is working"}), 200
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
