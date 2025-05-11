# Membuat Proyek Python Dapat Dipanggil Langsung dari Terminal

Salah satu fitur yang sangat berguna dalam pengembangan aplikasi Python adalah kemampuan untuk menjalankan aplikasi Anda sebagai perintah langsung dari terminal, tanpa perlu mengetik `python nama_file.py` atau `poetry run nama_perintah`. Ini membuat aplikasi Anda terasa lebih seperti alat baris perintah (CLI) asli.

Proses ini biasanya melibatkan pendefinisian "titik masuk" (entry points) atau "skrip konsol" (console scripts) dalam file konfigurasi proyek Anda, yaitu `pyproject.toml`.

## Mengapa Ini Berguna?

-   **Kemudahan Penggunaan**: Pengguna dapat menjalankan aplikasi Anda dengan perintah yang singkat dan mudah diingat.
-   **Integrasi**: Mudah diintegrasikan ke dalam skrip shell atau alur kerja otomatis lainnya.
-   **Distribusi**: Saat Anda mendistribusikan paket Python Anda (misalnya melalui PyPI), pengguna yang menginstalnya akan secara otomatis mendapatkan perintah ini di sistem mereka.

## Langkah-langkah Menggunakan `pyproject.toml`

Berikut adalah cara Anda dapat mengkonfigurasi proyek Python Anda agar dapat dipanggil langsung dari terminal menggunakan file `pyproject.toml`, yang merupakan standar modern untuk konfigurasi proyek Python (digunakan oleh alat seperti Poetry, Flit, atau build system berbasis PEP 517/518).

### 1. Struktur Proyek (Contoh)

Misalkan Anda memiliki struktur proyek seperti ini:

```
nama_proyek_anda/
├── pyproject.toml
├── README.md
└── src/
    └── nama_paket_anda/
        ├── __init__.py
        └── main.py  # Atau cli.py, atau nama file lain yang berisi fungsi utama
```

### 2. Buat Fungsi Titik Masuk (Entry Point Function)

Di dalam salah satu modul Python Anda (misalnya, `src/nama_paket_anda/main.py`), Anda perlu memiliki fungsi utama yang akan dieksekusi ketika perintah Anda dipanggil.

**Contoh `src/nama_paket_anda/main.py`:**

```python
import click # Contoh menggunakan Click untuk CLI yang lebih baik

@click.group()
def cli():
    """Sebuah contoh alat CLI yang luar biasa."""
    pass

@cli.command()
@click.option('--count', default=1, help='Jumlah salam.')
@click.argument('name')
def sapa(name: str, count: int):
    """Menyapa seseorang."""
    for _ in range(count):
        click.echo(f"Halo, {name}!")

def main_entry():
    """
    Fungsi ini akan menjadi titik masuk utama yang didefinisikan
    dalam pyproject.toml.
    """
    cli()

if __name__ == "__main__":
    main_entry()
```
Dalam contoh di atas, `main_entry()` adalah fungsi yang akan kita tunjuk dari `pyproject.toml`. Fungsi ini kemudian memanggil grup perintah `click`.

### 3. Konfigurasi `pyproject.toml`

Buka file `pyproject.toml` Anda dan tambahkan atau modifikasi bagian `[project.scripts]`. Ini adalah bagian standar yang didefinisikan dalam PEP 621.

```toml
[project]
name = "nama-paket-anda"  # Nama paket Anda di PyPI
version = "0.1.0"
description = "Deskripsi singkat tentang proyek Anda."
authors = [
    {name = "Nama Anda", email = "email@anda.com"}
]
requires-python = ">=3.8"
dependencies = [
    "click>=8.0", # Jika Anda menggunakan Click
    # dependensi lain...
]
# ... bagian lain dari [project] ...

# Ini adalah bagian penting!
[project.scripts]
nama-perintah-anda = "nama_paket_anda.main:main_entry"

# Jika Anda menggunakan Poetry, Anda mungkin juga memiliki bagian [tool.poetry.scripts]
# yang memiliki format serupa:
# [tool.poetry.scripts]
# nama-perintah-anda = "nama_paket_anda.main:main_entry"
# Poetry akan menerjemahkan ini ke [project.scripts] saat membangun.
# Untuk kompatibilitas yang lebih luas, [project.scripts] lebih disarankan.

[build-system]
requires = ["poetry-core>=1.0.0"] # Atau setuptools, flit_core, dll.
build-backend = "poetry.core.masonry.api" # Atau backend build lainnya
```

**Penjelasan bagian `[project.scripts]`:**

-   **`nama-perintah-anda`**: Ini adalah nama yang ingin Anda ketik di terminal untuk menjalankan aplikasi Anda (misalnya, `cv-builder`, `proyekku`, `alat-hebat`).
-   **`"nama_paket_anda.main:main_entry"`**: Ini adalah string yang menunjuk ke fungsi Python yang akan dijalankan.
    -   `nama_paket_anda.main`: Ini adalah path modul Python. Artinya, Python akan mencari file `main.py` di dalam direktori paket `nama_paket_anda` (yang biasanya ada di `src/nama_paket_anda/`).
    -   `:main_entry`: Ini adalah nama fungsi di dalam modul `main.py` yang akan dieksekusi.

### 4. Build dan Instal Proyek Anda

Setelah Anda mengkonfigurasi `pyproject.toml` dan menulis fungsi titik masuk Anda, Anda perlu membangun dan menginstal paket Anda. Proses instalasi inilah yang akan membuat skrip _executable_ dan menempatkannya di lokasi yang dapat dijangkau oleh `PATH` sistem Anda.

**Menggunakan Poetry:**

```bash
# Dari direktori root proyek Anda
poetry install
```
Perintah ini akan menginstal paket Anda ke dalam lingkungan virtual yang dikelola oleh Poetry, dan skrip perintah akan tersedia saat lingkungan tersebut aktif.

Untuk instalasi yang lebih "global" (atau ke lingkungan Python utama Anda, jika tidak menggunakan virtual environment secara ketat):
```bash
poetry build
pip install dist/nama_paket_anda-0.1.0-py3-none-any.whl # Sesuaikan nama file .whl
```

**Menggunakan `pip` secara langsung (dengan `setuptools` atau `flit` sebagai build backend):**

```bash
# Dari direktori root proyek Anda
pip install .
```
Atau untuk mode pengembangan (perubahan pada kode sumber akan langsung terlihat tanpa perlu instal ulang):
```bash
pip install -e .
```

### 5. Jalankan Perintah Anda!

Setelah instalasi berhasil, Anda sekarang seharusnya dapat membuka terminal baru dan menjalankan perintah Anda secara langsung:

```bash
nama-perintah-anda sapa --count 3 "Dunia"
```

Output yang diharapkan:
```
Halo, Dunia!
Halo, Dunia!
Halo, Dunia!
```

## Kesimpulan

Dengan mendefinisikan skrip konsol di `pyproject.toml`, Anda dapat membuat aplikasi Python Anda lebih mudah diakses dan digunakan sebagai alat baris perintah. Ini adalah praktik standar dalam ekosistem Python modern dan sangat direkomendasikan untuk proyek yang dimaksudkan untuk digunakan sebagai CLI.
