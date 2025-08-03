import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import tempfile
import json

from resume_analyzer import ResumeAnalyzer
from file_processor import FileProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize components
file_processor = FileProcessor()
resume_analyzer = ResumeAnalyzer()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PDF or DOCX files only.', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename or '')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        extracted_text = file_processor.extract_text(filepath)
        if not extracted_text.strip():
            flash('Could not extract text from the file. Please ensure it contains readable text.', 'error')
            os.remove(filepath)  # Clean up
            return redirect(url_for('index'))
        
        # Analyze resume
        analysis_result = resume_analyzer.analyze_resume(extracted_text)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return render_template('results.html', 
                             analysis=analysis_result, 
                             original_text=extracted_text,
                             filename=filename)
    
    except Exception as e:
        logging.error(f"Error processing upload: {str(e)}")
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_optimized')
def download_optimized():
    """Download optimized resume content"""
    try:
        optimized_content = request.args.get('content', '')
        if not optimized_content:
            flash('No optimized content available', 'error')
            return redirect(url_for('index'))
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(optimized_content)
            temp_file_path = temp_file.name
        
        return send_file(temp_file_path, 
                        as_attachment=True, 
                        download_name='optimized_resume.txt',
                        mimetype='text/plain')
    
    except Exception as e:
        logging.error(f"Error creating download: {str(e)}")
        flash('Error creating download file', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logging.error(f"Internal server error: {str(e)}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
