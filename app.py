from flask import Flask, render_template, request, jsonify
import os
from PIL import Image
import pytesseract
import pdf2image

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Route for the Tubby Home Page
@app.route('/tubby')
def tubby():
    return render_template('tubby.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Generate feedback
    feedback = get_file_feedback(file_path)
    
    return jsonify({'message': feedback})

def get_file_feedback(file_path):
    try:
        if file_path.endswith('.pdf'):
            # Convert PDF to images
            images = pdf2image.convert_from_path(file_path)
            text = ''
            for img in images:
                text += pytesseract.image_to_string(img)
        else:
            # Process image
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        
        # Example feedback (you can adjust this based on your needs)
        return f"Extracted Text: {text[:150]}..."  # First 150 characters of extracted text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)