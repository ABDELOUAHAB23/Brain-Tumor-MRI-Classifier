from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Load and verify the model
try:
    model = tf.keras.models.load_model('Brain_Tumor_Model.h5')
    model.summary()
    
    # Print model input shape
    input_shape = model.input_shape
    output_shape = model.output_shape
    logger.info(f'Model input shape: {input_shape}')
    logger.info(f'Model output shape: {output_shape}')
    logger.info('Model loaded successfully')
    
    # Verify model with random data
    test_input = np.random.random((1, 224, 224, 3))
    test_pred = model.predict(test_input)
    logger.info(f'Test prediction shape: {test_pred.shape}')
    logger.info(f'Test prediction sample: {test_pred[0]}')
    
except Exception as e:
    logger.error(f'Error loading model: {str(e)}')
    raise

# Define class names and their descriptions
CLASS_NAMES = ['No Tumor', 'Glioma', 'Meningioma', 'Pituitary']
CLASS_DESCRIPTIONS = {
    'No Tumor': 'No brain tumor detected in the MRI scan.',
    'Glioma': 'A type of tumor that starts in the glial cells of the brain or spine.',
    'Meningioma': 'A tumor that forms on membranes that cover the brain and spinal cord inside the skull.',
    'Pituitary': 'A tumor that develops in the pituitary gland at the base of the brain.'
}

@app.route('/')
def index():
    return render_template('index.html')

def validate_image(file):
    # Check if file is actually an image
    try:
        # Save the current position
        file.seek(0)
        img = Image.open(file)
        # Just check if it's a valid image
        img.verify()
        # Reset file pointer
        file.seek(0)
        return True
    except Exception as e:
        logger.error(f'Image validation error: {str(e)}')
        return False

def preprocess_image(file):
    try:
        # Reset file pointer to start
        file.seek(0)
        
        # Open image
        img = Image.open(file)
        
        # Get image info
        width, height = img.size
        logger.info(f'Original image size: {width}x{height}, Mode: {img.mode}')
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
            logger.info(f'Converted image to RGB mode')
        
        # Resize to match model input size (224x224)
        img = img.resize((224, 224), Image.Resampling.LANCZOS)
        logger.info('Image resized to 224x224')
        
        # Convert to array and normalize
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        logger.info(f'Image array shape before expand_dims: {img_array.shape}')
        
        img_array = tf.expand_dims(img_array, 0)
        logger.info(f'Image array shape after expand_dims: {img_array.shape}')
        
        # Normalize and check values
        img_array = img_array / 255.0
        logger.info(f'Array value range after normalization: min={np.min(img_array)}, max={np.max(img_array)}')
        
        logger.info('Image preprocessing completed successfully')
        return img_array
    except Exception as e:
        logger.error(f'Error preprocessing image: {str(e)}')
        raise Exception(f'Error preprocessing image: {str(e)}')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if file was provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file has a name
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file extension
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        return jsonify({'error': 'Invalid file type. Allowed types: PNG, JPG, JPEG, GIF, BMP'}), 400
    
    # Validate file type
    if not validate_image(file):
        return jsonify({'error': 'Invalid or corrupted image file'}), 400
    
    try:
        # Preprocess the image
        processed_image = preprocess_image(file)
        
        # Make prediction with error handling
        try:
            # Log input shape before prediction
            logger.info(f'Input shape before prediction: {processed_image.shape}')
            logger.info(f'Input value range: min={np.min(processed_image)}, max={np.max(processed_image)}')
            
            # Make prediction
            prediction = model.predict(processed_image)
            logger.info(f'Raw prediction output: {prediction}')
            
        except Exception as e:
            logger.error(f'Model prediction error: {str(e)}')
            return jsonify({'error': 'Error during prediction'}), 500
        
        # Get predicted class and probabilities
        predicted_class_idx = np.argmax(prediction[0])
        predicted_class = CLASS_NAMES[predicted_class_idx]
        logger.info(f'Predicted class index: {predicted_class_idx}, class name: {predicted_class}')
        
        # Get probabilities for all classes
        probabilities = [float(p) * 100 for p in prediction[0]]
        logger.info('Class probabilities:')
        for class_name, prob in zip(CLASS_NAMES, probabilities):
            logger.info(f'{class_name}: {prob:.2f}%')
        
        # Prepare detailed response
        response = {
            'result': predicted_class,
            'description': CLASS_DESCRIPTIONS[predicted_class],
            'probabilities': {
                class_name: float(prob) 
                for class_name, prob in zip(CLASS_NAMES, probabilities)
            },
            'confidence_level': 'High' if max(probabilities) > 90 else 'Medium' if max(probabilities) > 70 else 'Low'
        }
        
        logger.info(f'Prediction completed: {predicted_class} with {max(probabilities):.2f}% confidence')
        return jsonify(response)
        
    except Exception as e:
        logger.error(f'Error processing request: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
