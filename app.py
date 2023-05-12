from flask import Flask, render_template, request, redirect, send_file
from PIL import Image
import os
import io

app = Flask(__name__)


# Fungsi untuk memastikan folder uploads tersedia
def create_uploads_folder():
    uploads_folder = 'uploads'
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compress', methods=['POST'])
def compress():
    if 'image' not in request.files:
        return redirect('/')

    image = request.files['image']
    if image.filename == '':
        return redirect('/')

    create_uploads_folder()  # Memastikan folder uploads tersedia

    # Simpan gambar yang diunggah ke server
    image_path = 'uploads/original.png'  # Simpan dalam format PNG
    image.save(image_path)

    # Kompresi gambar menggunakan Pillow library
    original_image = Image.open(image_path).convert('RGB')  # Konversi RGBA ke RGB
    compressed_image_path = 'uploads/compressed.jpg'
    original_image.save(compressed_image_path, optimize=True, quality=50)

    # Hapus gambar asli dari server
    os.remove(image_path)

    return redirect('/download')


@app.route('/download')
def download():
    return send_file('uploads/compressed.jpg', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
