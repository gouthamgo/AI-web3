from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React

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
    data = request.json
    prompt = data.get('prompt', '')
    
    # Get the generator instance (lazy loading)
    gen = get_generator()
    
    # Generate Solidity code with reduced max_length to save memory
    output = gen(prompt, max_length=100, num_return_sequences=1, truncation=True)
    solidity_code = output[0]['generated_text']
    
    return jsonify({'code': solidity_code})

if __name__ == '__main__':
    app.run(debug=True)