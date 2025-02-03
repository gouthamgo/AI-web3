from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)

# Enable CORS for Render.com deployment
# This is more permissive for Render's environment
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Lazy loading of the model
generator = None

def get_generator():
    global generator
    if generator is None:
        print("Loading model...")
        generator = pipeline('text-generation', model='distilgpt2')
    return generator

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'OK'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        gen = get_generator()
        output = gen(prompt, max_length=100, num_return_sequences=1, truncation=True)
        solidity_code = output[0]['generated_text']

        response = jsonify({'code': solidity_code})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = jsonify({'error': str(e)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500

@app.route('/health', methods=['GET'])
def health_check():
    response = jsonify({'status': 'healthy'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Add this for Render.com deployment
if __name__ == '__main__':
    # Use the port provided by Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)