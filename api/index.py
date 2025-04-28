from flask import Flask, request, send_file
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['POST'])
def convert_csv_to_txt():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    # Read CSV
    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.reader(stream)
    
    # Skip header
    next(reader, None)

    # Create TXT
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
