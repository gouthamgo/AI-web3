from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React

# Load a lightweight text-generation pipeline using distilgpt2
generator = pipeline('text-generation', model='distilgpt2')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    
    # Generate Solidity code with reduced max_length to save memory
    output = generator(prompt, max_length=100, num_return_sequences=1, truncation=True)
    solidity_code = output[0]['generated_text']
    
    return jsonify({'code': solidity_code})

if __name__ == '__main__':
    app.run(debug=True)