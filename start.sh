#!/bin/bash

# Jalankan skrip unduh model
echo "--- Menjalankan skrip unduh model ---"
python download_models.py

# Mulai server API
echo "--- Memulai server API FastAPI ---"
uvicorn main:app --host 0.0.0.0 --port 8000
