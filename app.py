from flask import Flask, render_template, request, redirect, url_for
import hashlib
import json
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
blockchain_file = 'blockchain.json'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
def load_blockchain():
    if os.path.exists(blockchain_file):
        with open(blockchain_file, 'r') as file:
            return json.load(file)
    return []
def save_blockchain():
    with open(blockchain_file, 'w') as file:
        json.dump(blockchain, file, indent=4)
blockchain = load_blockchain()
def create_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
def create_block(file_name, file_hash):
    block = {
        'file_name': file_name,
        'file_hash': file_hash,
        'previous_hash': blockchain[-1]['file_hash'] if blockchain else '0'
    }
    blockchain.append(block)
    save_blockchain()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload_document():
    file = request.files.get('file')
    if not file or file.filename == '':
        return render_template('result.html', message='❌ No file selected.')
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    file_hash = create_hash(file_path)
    create_block(file.filename, file_hash)
    return render_template('result.html', 
                           message='✅ File uploaded and added to blockchain.',
                           file_name=file.filename,
                           file_hash=file_hash)
@app.route('/verify', methods=['POST'])
def verify_document():
    file = request.files.get('file')
    if not file or file.filename == '':
        return render_template('result.html', message='❌ No file selected.')

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    file_hash = create_hash(file_path)

    for block in blockchain:
        if block['file_hash'] == file_hash:
            return render_template('result.html', 
                                   message='✅ File is valid and verified in blockchain.',
                                   file_name=file.filename,
                                   file_hash=file_hash)

    return render_template('result.html', 
                           message='⚠️ File not found in blockchain.',
                           file_name=file.filename,
                           file_hash=file_hash)

@app.route('/chain', methods=['GET'])
def view_blockchain():
    return render_template('chain.html', blockchain=blockchain)

if __name__ == '__main__':
    app.run(debug=True)








  

       
