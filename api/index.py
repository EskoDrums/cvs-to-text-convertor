from flask import Flask, request, send_file
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    try:
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

        # Return TXT directly
        return send_file(
            io.BytesIO(output.read().encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name='user_ids.txt'
        )

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
