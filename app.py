from flask import Flask, request, render_template, send_file
from PIL import Image
import pytesseract

app = Flask(__name__)

# Temporary storage for extracted text
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
last_extracted_text = None


@app.route("/", methods=["GET", "POST"])
def index():
    global last_extracted_text
    extracted_text = None

    if request.method == "POST":
        file = request.files["image"]
        if file:
            # Save uploaded image
            filepath =  file.filename
            file.save(filepath)

            # OCR with pytesseract
            image = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(image)

            # Save in global variable
            last_extracted_text = extracted_text

    return render_template("index.html", extracted_text=extracted_text)


@app.route("/download")
def download():
    global last_extracted_text
    if not last_extracted_text:
        return "No text available to download."

    filename = "extracted_text.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(last_extracted_text)

    return send_file(filename, as_attachment=True)





if __name__ == "__main__":
    app.run(debug=True)

