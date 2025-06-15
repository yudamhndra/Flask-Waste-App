import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import base64
import io
import json

template_dir = os.path.abspath('views/')
static_dir = os.path.abspath('resources/')

app = Flask(__name__, 
        template_folder=template_dir,
        static_folder=static_dir)

app.config['UPLOAD_FOLDER'] = os.path.abspath('resources/images')
app.config['RESULT_FOLDER'] = os.path.abspath('resources/images_results')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

try:
    model_path = os.path.abspath('model/mobilenet_best.h5')
    loaded_model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    loaded_model = None

class_labels = ['Cardboard', 'Food Organics', 'Glass', 'Metal', 'Miscellaneous Trash', 'Paper', 'Plastic', 'Textile Trash', 'Vegetation']

class_colors = {
    'Cardboard': '#8B4513',
    'Food Organics': '#228B22', 
    'Glass': '#00CED1',
    'Metal': '#C0C0C0',
    'Miscellaneous Trash': '#696969',
    'Paper': '#F5F5DC',
    'Plastic': '#FF6347',
    'Textile Trash': '#9370DB',
    'Vegetation': '#32CD32'
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_and_visualize(image_path):
    """
    Predict waste class and create visualization with bounding box
    """
    try:
        if loaded_model is None:
            return None, "Model not loaded"

        img = image.load_img(image_path, target_size=(512, 512))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        prediction = loaded_model.predict(img_array)
        predicted_class_idx = np.argmax(prediction[0])
        confidence = prediction[0][predicted_class_idx] * 100
        predicted_class = class_labels[predicted_class_idx]

        original_img = Image.open(image_path)
        img_width, img_height = original_img.size

        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax.imshow(original_img)
        ax.axis('off')

        box_width = img_width * 0.7
        box_height = img_height * 0.7
        box_x = (img_width - box_width) / 2
        box_y = (img_height - box_height) / 2

        color = class_colors.get(predicted_class, '#FF0000')
        rect = patches.Rectangle(
            (box_x, box_y), box_width, box_height,
            linewidth=4, edgecolor=color, facecolor='none'
        )
        ax.add_patch(rect)

        label_text = f"{predicted_class}\n{confidence:.1f}%"
        ax.text(
            box_x, box_y - 20, label_text,
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=color, alpha=0.8),
            color='white'
        )

        result_filename = f"result_{os.path.basename(image_path)}"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        plt.savefig(result_path, bbox_inches='tight', dpi=150)
        plt.close()  

        all_predictions = {}
        for i, (label, prob) in enumerate(zip(class_labels, prediction[0])):
            all_predictions[label] = float(prob * 100)
        
        result_data = {
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'all_predictions': all_predictions,
            'result_image': f"images_results/{result_filename}",
            'color': color
        }
        
        return result_data, None
        
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    """Homepage dengan form upload"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload dan prediction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        result, error = predict_and_visualize(file_path)
        
        if error:
            return jsonify({'error': error}), 500

        os.remove(file_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(static_dir, filename)

if __name__ == '__main__':
    print(f"Template folder: {template_dir}")
    print(f"Static folder: {static_dir}")
    print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Result folder: {app.config['RESULT_FOLDER']}")
    app.run(debug=True, host='0.0.0.0', port=5000)