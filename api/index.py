from flask import Flask, request, send_file, jsonify
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return jsonify({"message": "CSV to TXT API is live. Send a POST request with CSV file."})
    
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.reader(stream)
    
    next(reader, None)

    output = io.StringIO()
    for row in reader:
        if row:
            output.write(f"{row[0]}\n")

    output.seek(0)

    return send_file(
        io.BytesIO(output.read().encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name='user_ids.txt'
    )

if __name__ == "__main__":
    app.run()
