# Tes Junior Programmer - FastPrint Indonesia

Aplikasi manajemen produk berbasis web yang dikembangkan menggunakan **Django Framework** dan **PostgreSQL**.

Aplikasi ini dirancang untuk menyelesaikan tantangan teknis integrasi API dengan sistem autentikasi dinamis (Time-based Authentication), manajemen Cookie/Session, serta operasi CRUD database.

## 🚀 Fitur Unggulan

### 1. Smart API Integration (Backend Logic)

Fitur ini menjawab tantangan logika algoritma autentikasi username & password yang berubah setiap jam.

- **Auto-Sync Time:** Script otomatis mendeteksi waktu server (GMT) melalui Header HTTP dan mengonversinya ke zona waktu lokal (WIB) untuk menghasilkan Username yang valid (`C19`, `C20`, dst).
- **Session Management:** Menggunakan `requests.Session` untuk menangkap dan memelihara **Cookies** dari server agar request tidak ditolak.
- **Dynamic Password Hashing:** Generator MD5 otomatis berdasarkan format tanggal yang valid (`dd-mm-yy`).

### 2. Manajemen Data (CRUD)

- **Create & Update:** Form input dengan validasi otomatis (Django ModelForm).
- **Read:** Menampilkan daftar produk dengan filter otomatis status _"bisa dijual"_.
- **Delete:** Fitur hapus data dengan proteksi konfirmasi (JavaScript Confirm Alert).

### 3. Teknologi Database

- Menggunakan **PostgreSQL** sebagai database utama (Production Ready), menggantikan SQLite default.

## 🛠 Tech Stack

- **Backend:** Python 3.x, Django 5.x
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5 (Responsive UI)
- **HTTP Client:** Python Requests
- **Tools:** VS Code, pgAdmin 4

---

## 📦 Cara Instalasi & Menjalankan Project

Ikuti langkah-langkah berikut untuk menjalankan project di komputer lokal:

### 1. Clone Repository

```bash
git clone [https://github.com/USERNAME_GITHUB_ANDA/NAMA_REPO_ANDA.git]()
cd
```

### 2. Setup Virtual Environment

```bash
# Untuk Windows
python -m venv env
.\env\Scripts\activate

# Untuk Mac/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txtS
```

### 4. Konfigurasi Database (PostgreSQL)

1. Buka pgAdmin atau terminal PostgreSQL.

2. Buat database baru dengan nama: fastprint_db.

3. Buka file fastprint_tes/settings.py di project ini.

4. Sesuaikan bagian DATABASES dengan username & password PostgreSQL lokal Anda:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fastprint_db',
        'USER': 'postgres',
        'PASSWORD': 'password_postgres_anda',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Migrasi Database

```bash
python manage.py migrate
```

### 6. Import Data dari API

Jalankan custom command ini untuk menarik data dari API FastPrint, memproses autentikasi, dan menyimpannya ke database lokal.

```python
python manage.py import_data
```

### 7. Jalankan Server

```bash
python manage.py runserver
```

👤 Author
Hannes Tigor Hamonangan Sinaga
LinkedIn: https://www.linkedin.com/in/hannessinaga/
GitHub: https://github.com/N4CHT0
Email: hannessinaga77@gmail.com

Dibuat untuk memenuhi Tes Seleksi Junior Programmer FastPrint.
