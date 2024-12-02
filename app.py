from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Define directories for uploads and processed videos
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Serve the HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Handle video upload from the upload option
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)


# Handle live record video upload
@app.route('/upload-recorded', methods=['POST'])
def upload_recorded():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    input_path = os.path.join(PROCESSED_FOLDER, file.filename)
    file.save(input_path)


@app.route('/upscale-recorded', methods=['POST'])
def upscale_recorded():
    # Logic for upscaling the recorded video
    # Simulate returning a processed video URL
    return jsonify({'url': '/processed/upscaled_recorded_video.mp4'}), 200

@app.route('/upscale-uploaded', methods=['POST'])
def upscale_uploaded():
    # Logic for upscaling the uploaded video
    # Simulate returning a processed video URL
    return jsonify({'url': '/processed/upscaled_uploaded_video.mp4'}), 200



# Upscale video using FFmpeg
def upscale_video(input_path, output_path):
    subprocess.run([
        'ffmpeg', '-i', input_path, '-vf', 'scale=1920:1080', '-c:v', 'libx264', '-preset', 'fast',
        output_path
    ])

if __name__ == '__main__':
    app.run(debug=True)
