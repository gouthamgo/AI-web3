from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)

# Configure CORS in a more permissive way
CORS(app, 
     origins=["https://ai-web3.netlify.app"],
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type"],
     supports_credentials=True,
     max_age=3600)

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
    # Explicitly handle OPTIONS requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'https://ai-web3.netlify.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
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
        # Explicitly add CORS headers to the response
        response.headers.add('Access-Control-Allow-Origin', 'https://ai-web3.netlify.app')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    except Exception as e:
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', 'https://ai-web3.netlify.app')
        error_response.headers.add('Access-Control-Allow-Credentials', 'true')
        return error_response, 500

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    response = jsonify({'status': 'healthy'})
    response.headers.add('Access-Control-Allow-Origin', 'https://ai-web3.netlify.app')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)