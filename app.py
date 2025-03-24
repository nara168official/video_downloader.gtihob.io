import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pytube import YouTube
from yt_dlp import YoutubeDL
import config

app = Flask(__name__)
app.config.from_object(config)

# Ensure downloads directory exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

def download_youtube_video(url, quality='highest'):
    try:
        yt = YouTube(url)
        if quality == 'highest':
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.get_lowest_resolution()
        
        filename = secure_filename(f"{yt.title}.mp4")
        filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        stream.download(output_path=app.config['DOWNLOAD_FOLDER'], filename=filename)
        return filename
    except Exception as e:
        raise Exception(f"YouTube download error: {str(e)}")

def download_generic_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(app.config['DOWNLOAD_FOLDER'], '%(title)s.%(ext)s'),
            'quiet': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return os.path.basename(filename)
    except Exception as e:
        raise Exception(f"Video download error: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    platform = data.get('platform')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        if platform == 'youtube':
            filename = download_youtube_video(url)
        else:
            filename = download_generic_video(url)
        
        download_url = f"/downloads/{filename}"
        return jsonify({
            'success': True,
            'download_url': download_url,
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)