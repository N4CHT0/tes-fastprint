from django.core.management.base import BaseCommand
import requests
import hashlib
from datetime import datetime, timedelta
from produk_app.models import Produk, Kategori, Status

class Command(BaseCommand):
    help = 'Import data menggunakan Waktu Server & Cookies'

    def handle(self, *args, **kwargs):
        # URL API
        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        
        # 1. GUNAKAN SESSION (Untuk menyimpan Cookies otomatis)
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        })

        self.stdout.write("1. Menghubungi server untuk ambil Header & Cookie...")
        
        try:
            # Request pancingan (GET) untuk ambil Waktu Server & Cookie
            resp_init = session.head(url) # Head cuma ambil header, lebih cepat
            
            # Ambil Waktu Server dari Header 'Date'
            # Format biasanya: "Sat, 31 Jan 2026 14:00:00 GMT"
            server_date_str = resp_init.headers.get('Date')
            
            if not server_date_str:
                self.stdout.write(self.style.ERROR("Gagal ambil Header Date. Gunakan waktu laptop."))
                waktu_acuan = datetime.now()
            else:
                self.stdout.write(f"   Waktu Server (Raw): {server_date_str}")
                # Parse waktu server
                waktu_gmt = datetime.strptime(server_date_str, '%a, %d %b %Y %H:%M:%S %Z')
                # Konversi GMT ke WIB (GMT+7) karena FastPrint di Surabaya
                waktu_acuan = waktu_gmt + timedelta(hours=7)
                self.stdout.write(f"   Waktu Server (WIB): {waktu_acuan.strftime('%d-%m-%Y %H:%M:%S')}")

            # 2. GENERATE CREDENTIALS BERDASARKAN WAKTU SERVER
            # Password: bisacoding-31-01-26 (dd-mm-yy)
            pass_date = waktu_acuan.strftime("%d-%m-%y")
            password_raw = f"bisacoding-{pass_date}"
            password_md5 = hashlib.md5(password_raw.encode()).hexdigest()

            # Username: tesprogrammer + ddmmyy + C + Jam (WIB)
            user_date = waktu_acuan.strftime("%d%m%y")
            jam_wib = waktu_acuan.hour
            username = f"tesprogrammer{user_date}C{jam_wib:02d}"

            self.stdout.write(f"2. Login sebagai: {username}")
            # self.stdout.write(f"   Pass Mentah : {password_raw}")

            # 3. EKSEKUSI LOGIN (POST)
            # Session otomatis membawa cookie dari request pertama tadi
            payload = {'username': username, 'password': password_md5}
            response = session.post(url, data=payload)
            data_json = response.json()

            # Cek Error
            if 'error' in data_json and data_json['error'] == 1:
                self.stdout.write(self.style.ERROR(f"GAGAL: {data_json.get('ket')}"))
                return

            # Ambil Data
            items = data_json.get('data') or data_json.get('result') or []
            if not items:
                self.stdout.write(self.style.ERROR("Login sukses tapi data kosong!"))
                return

            self.stdout.write(self.style.SUCCESS(f"3. Sukses! Ditemukan {len(items)} data."))

            # 4. SIMPAN KE DATABASE
            count = 0
            for item in items:
                try:
                    # Clean Data
                    kat = item.get('kategori', 'Umum')
                    stat = item.get('status', 'Cek')
                    # Bersihkan harga dari string aneh
                    harga_str = str(item.get('harga', 0))
                    harga = int(''.join(filter(str.isdigit, harga_str))) if harga_str.strip() else 0

                    # Simpan (Get or Create)
                    kategori_obj, _ = Kategori.objects.get_or_create(nama_kategori=kat)
                    status_obj, _ = Status.objects.get_or_create(nama_status=stat)
                    
                    # Update or Create Produk
                    Produk.objects.update_or_create(
                        id_produk=int(item['id_produk']),
                        defaults={
                            'nama_produk': item['nama_produk'],
                            'harga': harga,
                            'kategori': kategori_obj,
                            'status': status_obj
                        }
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skip: {e}"))

            self.stdout.write(self.style.SUCCESS(f"SELESAI! {count} data tersimpan di PostgreSQL."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error Koneksi: {e}"))