import os
import requests
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './API')  # You can set this in environment variables
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'txt', 'pdf'}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint for file upload
@app.route('/API', methods=['POST'])
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

# New Endpoint for weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "City parameter is required"}), 400
    
    API_KEY = "your_api_key_here"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != 200:
            return jsonify({"error": data.get("message", "Error fetching weather data")}), 400
        
        return jsonify({
            "city": data["name"],
            "weather": data["weather"][0]["description"],
            "temperature": data["main"]["temp"] - 273.15,  # Convert Kelvin to Celsius
            "wind_speed": data["wind"]["speed"]
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
