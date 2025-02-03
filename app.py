from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for React

# Load a text-generation pipeline
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    
    # Generate Solidity code
    output = generator(prompt, max_length=200, num_return_sequences=1, truncation=True)
    solidity_code = output[0]['generated_text']
    
    return jsonify({'code': solidity_code})

if __name__ == '__main__':
    app.run(debug=True)