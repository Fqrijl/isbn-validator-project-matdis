from flask import Flask, render_template, request

app = Flask(__name__)

def is_valid_isbn10(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) != 10:
        return False
    total = 0
    for i, char in enumerate(isbn):
        if i == 9 and char.upper() == 'X':
            digit = 10
        elif char.isdigit():
            digit = int(char)
        else:
            return False
        total += (i + 1) * digit
    return total % 11 == 0

def is_valid_isbn13(isbn):
    isbn = isbn.replace("-", "").replace(" ", "")
    if len(isbn) != 13 or not isbn.isdigit():
        return False
    total = 0
    for i, digit in enumerate(isbn):
        digit = int(digit)
        total += digit * (1 if i % 2 == 0 else 3)
    return total % 10 == 0

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    if request.method == "POST":
        isbn = request.form["isbn"].strip()
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        if len(isbn_clean) == 10:
            valid = is_valid_isbn10(isbn)
            hasil = "ISBN-10 valid" if valid else "ISBN-10 tidak valid"
        elif len(isbn_clean) == 13:
            valid = is_valid_isbn13(isbn)
            hasil = "ISBN-13 valid" if valid else "ISBN-13 tidak valid"
        else:
            hasil = "ISBN harus 10 atau 13 digit angka"
    return render_template("index.html", hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)
