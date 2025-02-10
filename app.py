from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend fetch requests

# Define the folder to store uploaded files
UPLOAD_FOLDER = './API'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'json'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ File Upload Endpoint (POST method)
@app.route('/API/weather', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({
            "message": "File uploaded successfully!",
            "filename": file.filename
        }), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

# ✅ Weather Data Fetch Endpoint (GET method)
@app.route('/weather', methods=['GET'])
def get_weather():
    city_name = request.args.get('city')
    
    if not city_name:
        return jsonify({"error": "City parameter is required"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{city_name}.json")
    
    if not os.path.exists(file_path):
        return jsonify({"error": f"No weather data found for {city_name}"}), 404
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Root Endpoint
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the SkyCast API!"})

# ✅ Run the app
if __name__ == '__main__':
    print(f"Files will be uploaded to: {UPLOAD_FOLDER}")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
