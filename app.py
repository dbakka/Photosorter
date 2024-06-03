from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
from PIL import Image
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'selected_photos/'

# Ensure output and upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Define allowed file extensions, e.g., images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return "No file selected", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            return "File not allowed", 400
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Assumes a placeholder function for machine learning processing."""
    selected_photos, report = process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return f'Photos selected: {selected_photos}. Report generated: {report}'

def process_file(filepath):
    """Process the file to sort and select photos."""
    # Placeholder implementation
    return 10, '10 out of 100 photos selected.'

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    """Serve files from the output folder to the user."""
    return send_from_directory(directory=app.config['OUTPUT_FOLDER'], filename=filename)

@app.route('/test')
def test_route():
    """A simple route to test if the server is up and running."""
    return "Test route is working! If you're seeing this, Flask is configured correctly."

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "404 Error - The page cannot be found.", 404

@app.errorhandler(403)
def forbidden(e):
    """Return a custom 403 error."""
    return "403 Forbidden - You do not have permission to access this resource.", 403

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return "500 Internal Server Error - An unexpected error occurred.", 500

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
