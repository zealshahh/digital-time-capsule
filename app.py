from flask import Flask, request, render_template, jsonify
from PIL import Image, ImageFilter
import numpy as np
import cv2
import io

app = Flask(__name__)

def check_for_noise(image):
    # Convert to grayscale
    image_gray = image.convert("L")
    image_array = np.array(image_gray)

    # Apply Sobel edge detection
    edges = cv2.Sobel(image_array, cv2.CV_64F, 1, 1, ksize=3)
    edge_variance = np.var(edges)

    # Set a threshold for edge variance (higher variance suggests noise)
    noise_threshold = 50

    if edge_variance > noise_threshold:
        return 'Noisy'  # Image is noisy
    return 'Clean'  # Image is clean

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_image', methods=['POST'])
def check_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    try:
        image = Image.open(file)
        status = check_for_noise(image)
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
