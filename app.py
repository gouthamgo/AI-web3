from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
# Configure CORS with specific origins and options
CORS(app, resources={
    r"/generate": {  # Apply to /generate endpoint
        "origins": ["http://localhost:3000", "https://ai-web3.netlify.app/"],  
        "methods": ["POST"],  # Allow only POST method
        "allow_headers": ["Content-Type"],
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

@app.route('/generate', methods=['POST'])
def generate():
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

        return jsonify({'code': solidity_code}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)