from django.db import models

class Kategori(models.Model):
    # Ganti jadi AutoField agar ID dibuatkan otomatis (1, 2, 3...)
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_kategori

class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_status

class Produk(models.Model):
    # Tetap IntegerField karena kita pakai ID dari API (no. 6 tadi)
    id_produk = models.IntegerField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=15, decimal_places=0)
    
    # Relasi
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_produk