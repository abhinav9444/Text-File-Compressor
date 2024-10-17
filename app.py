import os
from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import huffman_coding

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Compress the file
        compressed_filename = f"compressed_{filename}.bin"
        compressed_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)
        original_size, compressed_size = huffman_coding.compress_file(file_path, compressed_path)
        
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        return jsonify({
            'message': 'File successfully uploaded and compressed',
            'compression_ratio': compression_ratio,
            'compressed_filename': compressed_filename
        })

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['COMPRESSED_FOLDER'], filename), as_attachment=True)

@app.route('/health-check')
def health_check():
    return "Server is running", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)