import io
from flask import Flask, request, redirect, send_from_directory, url_for, render_template, flash
from pymongo import MongoClient
from datetime import datetime, timedelta
from utils.parser import parse_log
from decrypter import decrypt_log  # Assuming decrypt_log is updated as per previous steps
import uuid
import gridfs
import os
import re

app = Flask(__name__)
app.config.from_object('config.Config')

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['log_parser_db']
fs = gridfs.GridFS(db)
parsed_collection = db['parsed_logs']

# Upload folder
UPLOAD_FOLDER = "/Users/abht/Desktop/Dart logs for parsing/uploads"
TOOL_PATH = "/Users/abht/Desktop/LogDecrypter/Mac"  # Path where the decryption tool is located

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ensure the TOOL_PATH exists
if not os.path.exists(TOOL_PATH):
    os.makedirs(TOOL_PATH)

def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def handle_decrypted_file(decrypted_filepath):
    """
    Parse the decrypted file and insert its data into MongoDB.
    
    Args:
        decrypted_filepath (str): Full path to the decrypted file.
    """
    try:
        # Parse the decrypted file
        parsed_data = parse_log(decrypted_filepath)
        print(f"Parsed Data: {parsed_data}")  # Debug: Print parsed data
        
        # Insert parsed data into MongoDB
        parsed_collection.delete_many({})  # Clear the collection before inserting new data
        for entry in parsed_data:
            parsed_collection.insert_one(entry)

        print("Parsed data successfully inserted into MongoDB.")
    except Exception as e:
        print(f"Error handling decrypted file: {e}")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload_encrypted', methods=['GET', 'POST'])
def upload_encrypted():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename, {'log'}):
            # Save the encrypted log file temporarily to TOOL_PATH
            encrypted_filename = f"{uuid.uuid4()}_{file.filename}"
            encrypted_filepath = os.path.join(TOOL_PATH, encrypted_filename)
            file.save(encrypted_filepath)

            # Construct decrypted file name
            decrypted_filename = f"{encrypted_filename.rsplit('.', 1)[0]}_decrypted.txt"
            decrypted_filepath = os.path.join(TOOL_PATH, decrypted_filename)

            try:
                # Decrypt the file
                decrypted_filepath = decrypt_log(encrypted_filepath, decrypted_filename)

                # Handle decrypted file (parse and store in MongoDB)
                handle_decrypted_file(decrypted_filepath)

                flash('File uploaded, decrypted, and parsed successfully!', 'success')
                return redirect(url_for('results'))
            except Exception as e:
                flash(f"An error occurred: {e}", 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Only .log files are allowed.', 'error')
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/results')
def results():
    entries = parsed_collection.find({}, {"_id": 0, "timestamp": 1, "requirement": 1, "status": 1}).sort("timestamp", -1)
    entries_list = list(entries)  # Convert cursor to list

     # Debugging print
    print("Fetched Entries from MongoDB (Debug):")
    for entry in entries_list:
        print(entry)  

    return render_template('results.html', entries=entries_list)


if __name__ == '__main__':
    app.run(debug=True)
