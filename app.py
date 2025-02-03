from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)

# Configure CORS to allow requests from your Netlify domain
CORS(app, resources={
    r"/*": {  # Apply to all routes
        "origins": ["https://ai-web3.netlify.app"],  # Your Netlify domain
        "methods": ["GET", "POST", "OPTIONS"],  # Allow these methods
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
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
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        prompt = data.get('prompt', '')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        # Get the generator instance (lazy loading)
        gen = get_generator()

        # Generate Solidity code
        output = gen(prompt, max_length=100, num_return_sequences=1, truncation=True)
        solidity_code = output[0]['generated_text']

        response = jsonify({'code': solidity_code})
        return response, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)