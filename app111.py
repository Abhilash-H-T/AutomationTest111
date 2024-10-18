# app.py

from flask import Flask, request, redirect, url_for, render_template, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from werkzeug.utils import secure_filename
from io import BytesIO
import os
import re

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Database Model
class ParsedEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), nullable=False)
    requirement = db.Column(db.String(300), nullable=False)
    result = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<ParsedEntry {self.id} - {self.requirement}: {self.result}>'

# WTForms Form for Uploading Files
class UploadForm(FlaskForm):
    file = FileField('Choose File', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def validate_file(form, field):
        if not allowed_file(field.data.filename):
            raise ValidationError('Only .txt files are allowed.')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash('File uploaded successfully!', 'success')
        parse_file(filepath)
        return redirect(url_for('results'))
    return render_template('index.html', form=form)

def parse_file(filepath):
    """
    Parses the uploaded file to extract Timestamp, Requirement, and Result.
    Stores the extracted data in the database.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    # Split entries by delimiter
    entries = content.strip().split('--------------------------------------------------------------------')

    # Regular expressions to extract required fields
    timestamp_pattern = re.compile(r'Timestamp:\s+(.*)')
    requirement_pattern = re.compile(r'Checking requirement:\s+\[(.*)\]:Mandatory')
    result_pattern = re.compile(r'Result:\s+\[.*\]:(.*)')

    for entry in entries:
        if entry.strip() == '':
            continue  # Skip empty entries

        timestamp_match = timestamp_pattern.search(entry)
        requirement_match = requirement_pattern.search(entry)
        result_match = result_pattern.search(entry)

        if timestamp_match and requirement_match and result_match:
            timestamp = timestamp_match.group(1).strip()
            requirement = requirement_match.group(1).strip()
            result = result_match.group(1).strip().upper()

            # Normalize result
            if result.startswith('PASSED'):
                result = 'PASSED'
            elif result.startswith('FAILED'):
                result = 'FAILED'
            else:
                result = 'UNKNOWN'

            # Debugging: Print parsed data
            print(f"Parsed Entry - Timestamp: {timestamp}, Requirement: {requirement}, Result: {result}")

            # Create a new ParsedEntry and add to the database
            new_entry = ParsedEntry(
                timestamp=timestamp,
                requirement=requirement,
                result=result
            )
            db.session.add(new_entry)
    db.session.commit()

@app.route('/results')
def results():
    entries = ParsedEntry.query.order_by(ParsedEntry.id.desc()).all()
    print(f"Number of entries passed to template: {len(entries)}")  # Debugging
    return render_template('results.html', entries=entries)

@app.route('/download/<int:entry_id>')
def download_file(entry_id):
    entry = ParsedEntry.query.get_or_404(entry_id)
    # Create a downloadable text representation of the entry
    file_content = f"Timestamp: {entry.timestamp}\nChecking requirement: [{entry.requirement}]:Mandatory\nResult: [{entry.requirement}]:{entry.result}\n"
    return send_file(
        BytesIO(file_content.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=f"{entry.requirement}.txt"
    )

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = ParsedEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Entry deleted successfully!', 'success')
    return redirect(url_for('results'))

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

