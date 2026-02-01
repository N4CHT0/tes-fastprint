from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max # <--- PENTING: Untuk mencari ID terakhir
from .models import Produk
from .forms import ProdukForm

# 1. HALAMAN UTAMA (READ)
def index(request):
    # Filter hanya menampilkan produk dengan status "bisa dijual"
    # Menggunakan __icontains agar tidak sensitif huruf besar/kecil
    produk_list = Produk.objects.filter(status__nama_status__icontains='bisa dijual').order_by('id_produk')
    
    context = {
        'produk_list': produk_list,
        'title': 'Daftar Produk'
    }
    return render(request, 'produk_app/index.html', context)

# 2. TAMBAH DATA (CREATE) - DENGAN AUTO ID
def tambah(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            # Tahan dulu, jangan save ke database
            produk_baru = form.save(commit=False)
            
            # --- LOGIKA AUTO INCREMENT MANUAL ---
            # Cari angka id_produk terbesar yang ada di database saat ini
            max_id = Produk.objects.aggregate(Max('id_produk'))['id_produk__max']
            
            # Jika database kosong, mulai dari 1. Jika ada, ambil max + 1
            if max_id is None:
                new_id = 1
            else:
                new_id = max_id + 1
                
            # Pasang ID baru ke produk yang mau disimpan
            produk_baru.id_produk = new_id
            
            # Sekarang aman untuk disimpan karena ID sudah terisi
            produk_baru.save()
            
            return redirect('index')
    else:
        form = ProdukForm()
    
    return render(request, 'produk_app/form.html', {'form': form, 'title': 'Tambah Produk'})

# 3. EDIT DATA (UPDATE)
def edit(request, id_produk):
    # Ambil data berdasarkan ID, jika tidak ada tampilkan 404
    produk = get_object_or_404(Produk, id_produk=id_produk)
    
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        # Isi form dengan data lama
        form = ProdukForm(instance=produk)
    
    return render(request, 'produk_app/form.html', {'form': form, 'title': 'Edit Produk'})

# 4. HAPUS DATA (DELETE)
def hapus(request, id_produk):
    produk = get_object_or_404(Produk, id_produk=id_produk)
    produk.delete()
    return redirect('index')