from flask import Flask, request, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# Define the folder to store uploaded files
UPLOAD_FOLDER = './API'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'txt', 'pdf', 'json'}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint for file upload (POST method)
@app.route('/API/weather', methods=['POST'])
def upload_file():
    # Check if 'file' is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file type is allowed
    if file and allowed_file(file.filename):
        # Define the file path to save the file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # Save the file
        file.save(filename)
        return jsonify({
            "message": "File uploaded successfully!",
            "filename": file.filename
        }), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

# Endpoint to list uploaded files (GET method)
@app.route('/weather', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"files": files}), 200

# Run the app
if __name__ == '__main__':
    print(f"Files will be uploaded to: {UPLOAD_FOLDER}")
    app.run(debug=True)
