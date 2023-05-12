# Import library yang dibutuhkan
import cv2
import numpy as np
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

# Membuat objek aplikasi Flask
app = Flask(__name__)

# Fungsi untuk menghapus watermark pada gambar
def remove_watermark(image):
    # Mengambil gambar dengan OpenCV
    img = cv2.imread(image)
    # Mengubah ukuran gambar dengan resize()
    resized_img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
    # Membuat duplikat gambar dan membuat semua piksel menjadi putih
    copy_img = img.copy()
    copy_img[:]=(255,255,255)
    # Mengonversi gambar dari RGB ke HSV
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Mengubah ukuran gambar HSV
    resized_imghsv = cv2.resize(imghsv, (0,0), fx=0.2, fy=0.2)
    # Menentukan rentang warna biru pada skala HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # Membuat mask untuk range warna biru dengan inRange()
    mask = cv2.inRange(imghsv, lower_blue, upper_blue)
    # Menghapus watermark dari gambar dengan bitwise and menggunakan mask yang sudah dibuat
    res_white = cv2.bitwise_and(copy_img, copy_img, mask = mask)
    # Menambahkan hasil penghapusan watermark ke gambar asli
    res = cv2.add(img, res_white)
    # Mengubah ukuran gambar hasil
    resized_res = cv2.resize(res, (0,0), fx=0.2, fy=0.2)
    # Menyimpan gambar yang sudah dihapus watermarknya
    cv2.imwrite('hasil.jpg', resized_res)
    # Mengembalikan nama file hasil penghapusan watermark
    return 'hasil.jpg'

# Fungsi untuk menampilkan halaman utama
@app.route('/')
def index():
    # Menampilkan halaman index.html
    return render_template('index.html')

# Fungsi untuk mengunggah file
@app.route('/', methods=['POST'])
def upload_file():
    # Memeriksa apakah file sudah diunggah atau belum
    file = request.files['file']
    # Mengamankan nama file dengan menggunakan secure_filename()
    filename = secure_filename(file.filename)
    # Menyimpan file yang sudah diunggah
    file.save(filename)
    # Memanggil fungsi remove_watermark() untuk menghapus watermark pada gambar
    result = remove_watermark(filename)
    # Mengunduh hasil penghapusan watermark
    return download(result)

# Fungsi untuk men-download file
@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Mengirim file ke pengguna
    return send_file(filename, as_attachment=True)