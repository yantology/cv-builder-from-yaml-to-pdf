# Contoh Penggunaan Dependensi dalam Proyek

Dokumen ini memberikan contoh bagaimana setiap dependensi utama dalam proyek `cv-builder-from-yaml-to-pdf` digunakan dalam kode. Ini melengkapi dokumen `dependencies.md` yang menjelaskan apa itu setiap dependensi.

## 1. Click (`click>=8.1.3`)

Click digunakan untuk membuat antarmuka baris perintah (CLI) yang interaktif dan mudah digunakan.

**File Penggunaan Utama:** `src/cv_builder_from_yaml_to_pdf/main.py`

**Deskripsi Singkat Penggunaan:**
Click dipakai untuk mendefinisikan grup perintah, perintah individual (seperti `generate`, `init`, `validate`), argumen yang diterima perintah, dan opsi-opsi yang dapat menyertainya. Ini juga menangani pembuatan pesan bantuan secara otomatis.

**Contoh Kode:**
```python
# Potongan dari src/cv_builder_from_yaml_to_pdf/main.py
import click
import sys
from typing import Optional

@click.group()
def cli():
    """CV Builder: Convert YAML files to beautiful PDF CVs."""
    pass

@cli.command('generate')
@click.argument('yaml_file', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('--output', '-o', type=click.Path(file_okay=True, dir_okay=False, writable=True),
              help='Output PDF file path.')
@click.option('--style', '-s', type=click.Choice([
    'classic', 'modern', 'minimal'], case_sensitive=False),
              default='classic', help='Style for the CV (classic, modern, or minimal).')
# ... opsi lainnya ...
def generate_command(yaml_file: str, output: Optional[str] = None, style: str = 'classic', 
                     page_size: str = 'A4', preview: bool = False):
    """Generate a PDF CV from a YAML file.
    
    YAML_FILE: Path to the YAML file containing CV data.
    """
    try:
        # ... logika perintah generate ...
        click.echo(f"Successfully generated PDF CV: {{pdf_path}}")
        if preview:
            # ... logika preview ...
            pass
    except Exception as e:
        click.echo(f"An unexpected error occurred: {{e}}", err=True)
        sys.exit(1)

# ... perintah lainnya seperti init, validate, schema ...

def main():
    """Entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()
```
**Penjelasan Singkat:**
- `@click.group()` membuat `cli` sebagai grup perintah utama.
- `@cli.command('generate')` mendaftarkan `generate_command` sebagai sub-perintah `generate`.
- `@click.argument(...)` mendefinisikan argumen posisi seperti `yaml_file`.
- `@click.option(...)` mendefinisikan opsi seperti `--output` dan `--style`.
- `click.echo()` digunakan untuk mencetak output ke konsol, dengan dukungan untuk output standar dan error (`err=True`).

## 2. PyYAML (`pyyaml>=6.0`)

PyYAML digunakan untuk membaca (parsing) dan menulis (emitting) data dalam format YAML.

**File Penggunaan Utama:** `src/cv_builder_from_yaml_to_pdf/yaml_parser.py` (untuk parsing)
**File Penggunaan Lain:** `src/cv_builder_from_yaml_to_pdf/main.py` (untuk menangani `yaml.YAMLError`)

**Deskripsi Singkat Penggunaan:**
Dalam proyek ini, PyYAML terutama digunakan untuk membaca file CV `.yaml` yang disediakan pengguna dan mengubahnya menjadi struktur data Python (dictionary) agar bisa divalidasi dan diproses lebih lanjut untuk pembuatan PDF.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/yaml_parser.py` (diasumsikan):**
```python
# src/cv_builder_from_yaml_to_pdf/yaml_parser.py
import yaml
from typing import Dict, Any

def parse_yaml_file(file_path: str) -> Dict[str, Any]:
    """Parses a YAML file and returns its content as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                # CV data diharapkan berupa mapping di level teratas
                raise ValueError("YAML root content must be a mapping (dictionary).")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: YAML file not found at {{file_path}}")
    except yaml.YAMLError as e:
        # Menangkap dan meneruskan error spesifik dari PyYAML
        raise yaml.YAMLError(f"Error parsing YAML file {{file_path}}: {{e}}")
```
**Penjelasan Singkat:**
- `yaml.safe_load(f)` digunakan untuk mem-parsing stream dari file YAML (`f`) dengan aman. Ini mencegah eksekusi kode arbitrer yang mungkin ada dalam file YAML yang tidak tepercaya.
- Error seperti `FileNotFoundError` dan `yaml.YAMLError` ditangani untuk memberikan umpan balik yang jelas.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/main.py` (penanganan error):**
```python
# Potongan dari src/cv_builder_from_yaml_to_pdf/main.py
# ...
    except yaml.YAMLError as e:
        click.echo(f"Error: {{e}}", err=True)
        sys.exit(1)
# ...
```
**Penjelasan Singkat:**
Blok `try...except` di `main.py` menangkap `yaml.YAMLError` yang mungkin dilempar oleh `parse_yaml_file` jika ada masalah saat parsing YAML.

## 3. Pydantic (`pydantic>=2.11.4,<3.0.0`)

Pydantic digunakan untuk validasi data dan manajemen model data menggunakan anotasi tipe Python.

**File Penggunaan Utama:**
- `src/cv_builder_from_yaml_to_pdf/models.py` (untuk mendefinisikan model data CV)
- `src/cv_builder_from_yaml_to_pdf/main.py` (untuk memvalidasi data yang diparsing dari YAML)
- `src/cv_builder_from_yaml_to_pdf/schema.py` (untuk menghasilkan JSON Schema dari model)

**Deskripsi Singkat Penggunaan:**
Pydantic mendefinisikan struktur data yang diharapkan untuk CV (misalnya, field apa saja yang ada, tipe datanya, apakah wajib diisi). Ketika data dari file YAML dibaca, data tersebut divalidasi terhadap model Pydantic ini. Jika ada ketidaksesuaian, Pydantic akan menghasilkan error yang deskriptif.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/models.py`:**
```python
# src/cv_builder_from_yaml_to_pdf/models.py
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, HttpUrl, Field, field_validator

class PersonalInfo(BaseModel):
    name: str = Field(description="Full name.")
    email: EmailStr = Field(description="Email address.")
    phone: Optional[str] = Field(default=None, description="Phone number.")
    location: Optional[str] = Field(default=None, description="Current location (e.g., City, Country).")
    website: Optional[HttpUrl] = Field(default=None, description="Link to personal website or portfolio.")
    # ... field lainnya ...

class EducationEntry(BaseModel):
    institution: str
    degree: str
    start_date: str # Bisa juga Pydantic.AwareDatetime atau custom type
    end_date: Optional[str] = None
    details: Optional[List[str]] = Field(default_factory=list)

class CV(BaseModel):
    personal_info: PersonalInfo = Field(description="Personal contact information.")
    education: List[EducationEntry] = Field(default_factory=list, description="List of educational qualifications.")
    experience: List[Dict[str, Any]] = Field(default_factory=list) # Contoh jika experience lebih fleksibel
    skills: Optional[Dict[str, List[str]]] = Field(default_factory=dict)
    # ... field dan model lainnya ...
```
**Penjelasan Singkat (`models.py`):**
- Kelas seperti `PersonalInfo`, `EducationEntry`, dan `CV` mewarisi `BaseModel` dari Pydantic.
- Anotasi tipe (misalnya, `str`, `EmailStr`, `Optional[HttpUrl]`, `List[EducationEntry]`) digunakan untuk mendefinisikan tipe data yang diharapkan.
- `Field` digunakan untuk memberikan metadata tambahan seperti deskripsi atau nilai default.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/main.py` (validasi data):**
```python
# Potongan dari src/cv_builder_from_yaml_to_pdf/main.py
# ...
        # (Setelah cv_data_dict diparsing dari YAML oleh parse_yaml_file)
        from cv_builder_from_yaml_to_pdf.models import CV
        
        # Validasi dan konversi dictionary ke objek CV Pydantic
        try:
            cv_data = CV.model_validate(cv_data_dict) # Untuk Pydantic v2+
            # Untuk Pydantic v1: cv_data = CV(**cv_data_dict) atau CV.parse_obj(cv_data_dict)
        except ValidationError as e: # ValidationError dari Pydantic
            click.echo("Error: The YAML file contains validation errors:", err=True)
            for error in e.errors(): # e.errors() memberikan detail error
                loc = " -> ".join(map(str, error['loc']))
                msg = error['msg']
                click.echo(f"  - At '{loc}': {{msg}}", err=True)
            sys.exit(1)
# ...
```
**Penjelasan Singkat (`main.py` validasi):**
- `CV.model_validate(cv_data_dict)` (Pydantic v2+) mencoba membuat instance dari model `CV` menggunakan data dari dictionary. Proses ini secara otomatis melakukan validasi.
- Jika validasi gagal, `pydantic.ValidationError` akan muncul, dan detail error dapat diakses melalui `e.errors()`.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/schema.py` (generasi schema):**
```python
# Potongan dari src/cv_builder_from_yaml_to_pdf/schema.py
from typing import Dict, Any
from cv_builder_from_yaml_to_pdf.models import CV

def get_cv_schema() -> Dict[str, Any]:
    """Get the JSON schema for the CV model."""
    schema = CV.model_json_schema() # Untuk Pydantic v2+
    # Untuk Pydantic v1: schema = CV.schema()
    return schema
```
**Penjelasan Singkat (`schema.py`):**
- `CV.model_json_schema()` secara otomatis menghasilkan JSON Schema berdasarkan definisi model `CV` Pydantic.

## 4. ReportLab (`reportlab>=3.6.12`)

ReportLab adalah toolkit untuk membuat dokumen PDF secara programatik.

**File Penggunaan Utama:** `src/cv_builder_from_yaml_to_pdf/pdf_generator.py`

**Deskripsi Singkat Penggunaan:**
ReportLab digunakan untuk mengambil data CV yang sudah divalidasi (dalam bentuk objek Pydantic `CV`) dan menyusunnya menjadi dokumen PDF. Ini melibatkan pengaturan halaman, gaya teks, penambahan paragraf, gambar (jika ada), dan elemen lainnya ke dalam PDF.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/pdf_generator.py` (disederhanakan):**
```python
# src/cv_builder_from_yaml_to_pdf/pdf_generator.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import HexColor

from cv_builder_from_yaml_to_pdf.models import CV # Impor model CV
# Impor juga modul style kustom jika ada, misal:
# from .styles.modern_style import ModernStyle

def generate_cv_pdf(cv_data: CV, output_path: str, style_name: str = 'classic', page_size_str: str = 'A4'):
    if page_size_str.lower() == 'letter':
        current_page_size = letter
    else:
        current_page_size = A4

    doc = SimpleDocTemplate(output_path, pagesize=current_page_size,
                            leftMargin=1*inch, rightMargin=1*inch,
                            topMargin=1*inch, bottomMargin=1*inch)
    
    # Dapatkan stylesheet dasar atau kustom
    # styles = getSampleStyleSheet() # Dasar
    # Misal menggunakan style kustom:
    # active_style = ModernStyle() # Tergantung implementasi style Anda
    # styles = active_style.get_stylesheet()
    
    # Untuk contoh, kita gunakan stylesheet dasar
    styles = getSampleStyleSheet()
    story = []

    # --- Bagian Personal Info ---
    if cv_data.personal_info.name:
        story.append(Paragraph(cv_data.personal_info.name, styles['h1']))
    if cv_data.personal_info.email:
        story.append(Paragraph(f"Email: {{cv_data.personal_info.email}}", styles['Normal']))
    # ... tambahkan info personal lainnya ...
    story.append(Spacer(1, 0.2*inch))

    # --- Bagian Edukasi ---
    if cv_data.education:
        story.append(Paragraph("Education", styles['h2']))
        for edu in cv_data.education:
            story.append(Paragraph(f"<b>{{edu.institution}}</b> - {{edu.degree}}", styles['Normal']))
            story.append(Paragraph(f"<i>{{edu.start_date}} - {{edu.end_date or 'Present'}}</i>", styles['Italic']))
            if edu.details:
                for detail in edu.details:
                    story.append(Paragraph(f"• {{detail}}", styles['Bullet'])) # Asumsi ada style 'Bullet'
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.2*inch))

    # ... tambahkan bagian lain (Experience, Skills, etc.) ...

    try:
        doc.build(story)
    except Exception as e:
        raise RuntimeError(f"Failed to build PDF: {{e}}")
        
    return output_path
```
**Penjelasan Singkat:**
- `SimpleDocTemplate` membuat objek dokumen PDF.
- `Paragraph` digunakan untuk menambahkan teks dengan gaya tertentu (dari `getSampleStyleSheet()` atau stylesheet kustom).
- `Spacer` digunakan untuk menambahkan spasi vertikal.
- `story` adalah list yang berisi semua elemen (`Flowables`) yang akan digambar di PDF.
- `doc.build(story)` akhirnya membangun dokumen PDF dari `story`.

## 5. Jinja2 (`jinja2>=3.1.2`)

Jinja2 adalah mesin templat yang digunakan untuk menghasilkan file teks, dalam kasus ini, file YAML template.

**File Penggunaan Utama:** `src/cv_builder_from_yaml_to_pdf/templates.py` (atau modul yang bertanggung jawab atas manajemen templat, seperti `template_manager.py` jika ada).

**Deskripsi Singkat Penggunaan:**
Ketika pengguna menjalankan perintah `cv-builder init`, Jinja2 digunakan untuk memuat file templat YAML dasar (misalnya, `default.yaml`, `academic.yaml`) dan merendernya. Proses render ini mungkin melibatkan penggantian placeholder sederhana atau logika yang lebih kompleks jika templat membutuhkannya, meskipun untuk templat YAML CV awal mungkin tidak banyak variabel yang perlu di-render.

**Contoh Kode dari `src/cv_builder_from_yaml_to_pdf/templates.py` (diasumsikan):**
```python
# src/cv_builder_from_yaml_to_pdf/templates.py
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Asumsikan templat YAML disimpan di src/cv_builder_from_yaml_to_pdf/templates/yaml_templates/
TEMPLATE_DIR = Path(__file__).parent / "templates" / "yaml_templates"

if not TEMPLATE_DIR.is_dir():
    # Fallback jika struktur sedikit berbeda atau untuk debugging
    # Ini mungkin perlu disesuaikan berdasarkan struktur aktual Anda
    alt_template_dir = Path(__file__).resolve().parent.parent / "templates" / "yaml_templates"
    if alt_template_dir.is_dir():
        TEMPLATE_DIR = alt_template_dir
    else:
        # Jika direktori template tidak ditemukan, ini akan menyebabkan error saat Environment dibuat.
        # Anda bisa menangani ini dengan lebih baik, misal dengan exception kustom.
        print(f"Warning: Template directory not found at {{TEMPLATE_DIR}} or {{alt_template_dir}}")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['yaml']) # Meskipun untuk YAML, autoescape mungkin tidak terlalu relevan
)

def create_yaml_from_template(template_type: str, output_file_path: str) -> str:
    """
    Creates a new CV YAML file from a specified template type.
    """
    template_file_name = f"{{template_type}}.yaml"
    
    try:
        template = env.get_template(template_file_name)
    except Exception as e: # Lebih spesifik: jinja2.exceptions.TemplateNotFound
        available_templates = [f.name for f in TEMPLATE_DIR.glob('*.yaml') if f.is_file()]
        raise ValueError(
            f"Template '{{template_file_name}}' not found in {{TEMPLATE_DIR}}.\n"
            f"Available templates: {{available_templates or 'None found'}}. Error: {{e}}"
        )

    # Anda bisa meneruskan konteks ke template jika diperlukan
    # Misalnya: context = {'default_name': 'Your Name Here'}
    # rendered_yaml = template.render(context)
    rendered_yaml = template.render() # Jika template tidak memerlukan konteks

    output_path = Path(output_file_path)
    # Pastikan direktori output ada
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_yaml)
    
    return str(output_path.absolute())

```
**Penjelasan Singkat:**
- `Environment` dari Jinja2 disiapkan dengan `FileSystemLoader` yang menunjuk ke direktori tempat templat YAML disimpan.
- `env.get_template(template_file_name)` memuat templat yang diminta.
- `template.render()` menghasilkan konten akhir dari templat. Ini bisa menerima argumen keyword untuk mengisi placeholder di dalam templat.
- Konten yang sudah di-render kemudian ditulis ke file output.

Dengan memahami contoh-contoh ini, Anda seharusnya mendapatkan gambaran yang lebih baik tentang bagaimana setiap dependensi berkontribusi pada fungsionalitas keseluruhan aplikasi `cv-builder`.
