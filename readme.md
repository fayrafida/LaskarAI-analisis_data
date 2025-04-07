# Dashboard Project

## Setup Environment

### Persiapan Awal
1. Download file project dalam bentuk `.zip`.
2. Ekstrak file zip ke folder yang diinginkan.

### Setup Menggunakan Anaconda
1. Buka Anaconda Prompt.
2. Arahkan ke folder project hasil ekstrak:
   ```bash
   cd path/ke/folder/project
   ```
3. Buat environment baru dan install dependencies:
	```bash
	conda create -n dashboard-env --file requirements.txt
	conda activate dashboard-env
	```
### Setup Menggunakan Shell/Terminal (tanpa Anaconda)

1.  Buka terminal atau command prompt.
2.  Arahkan ke folder project hasil ekstrak:
	```bash
	cd path/ke/folder/project
	```
3. Buat virtual environment dan install dependencies:
	```bash
	python -m venv venv
	source venv/bin/activate   # Linux/MacOS
	venv\Scripts\activate      # Windows
	pip install -r requirements.txt
	```
## Menjalankan Aplikasi Dashboard

Jalankan perintah berikut di terminal:
```bash
streamlit run dashboard.py
```
