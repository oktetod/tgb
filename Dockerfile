# Menggunakan image dasar Python yang ringan
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Menyalin file aplikasi dan dependensi
COPY telegram_bot.py .
COPY requirements.txt .

# Menginstal dependensi Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Mendefinisikan port untuk aplikasi
EXPOSE 8080

# Menjalankan aplikasi Flask dengan Gunicorn
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "telegram_bot:app"]
