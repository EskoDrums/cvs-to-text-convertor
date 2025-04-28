from flask import Flask, request, jsonify, send_from_directory
import csv
import io
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'  # Vercel only allows /tmp to save files

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return jsonify({"message": "CSV to TXT API is live. Send POST request with CSV file."})

    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    try:
        # Read CSV
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        reader = csv.reader(stream)

        # Skip header (first line)
        next(reader, None)

        # Write TXT content to /tmp/user_ids.txt
        filepath = os.path.join(UPLOAD_FOLDER, 'user_ids.txt')
        with open(filepath, 'w', encoding='utf-8') as f:
            for row in reader:
                if row:
                    f.write(f"{row[0]}\n")

        # Return public link
        public_url = request.url_root.rstrip('/') + '/user_ids.txt'
        return jsonify({"file_url": public_url})

    except Exception as e:
        return f"Error while processing file: {str(e)}", 500

@app.route('/user_ids.txt', methods=['GET'])
def download_file():
    return send_from_directory(UPLOAD_FOLDER, 'user_ids.txt', mimetype='text/plain', as_attachment=True)

if __name__ == "__main__":
    app.run()
