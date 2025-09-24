# Juggernaut SDXL API di Saturn Cloud

Repositori ini berisi kode untuk men-deploy model AI Juggernaut SDXL sebagai API di Saturn Cloud, lengkap dengan dukungan untuk LoRA dan ControlNet.

## Cara Deploy di Saturn Cloud

1.  **Buat Proyek Baru**: Masuk ke akun Saturn Cloud Anda dan buat proyek baru.
2.  **Buat *Deployment* Baru**:
    * Di dalam proyek, klik **New** > **Deployment**.
    * Berikan nama, misalnya `juggernaut-api`.
3.  **Hubungkan GitHub**:
    * Di bagian **Image**, pilih **From a Git Repository**.
    * Masukkan URL repositori GitHub Anda ini.
4.  **Pilih Hardware**:
    * Pilih **Instance Type** yang memiliki GPU. **T4** (16GB GPU RAM) adalah pilihan awal yang baik. Model SDXL membutuhkan VRAM yang cukup besar.
5.  **Atur Perintah Startup**:
    * Di bagian **Command**, masukkan: `bash start.sh`
    * Ini akan memastikan skrip unduh model dijalankan sebelum server API dimulai.
6.  **Atur Port**:
    * Pastikan **Port** diatur ke `8000`.
7.  **Mulai Deployment**:
    * Klik **Create**. Saturn Cloud akan mulai membangun lingkungan Anda. Proses ini bisa memakan waktu lama pada saat pertama kali karena harus mengunduh semua model.
8.  **Dapatkan URL API**:
    * Setelah *deployment* berjalan, Saturn Cloud akan memberikan Anda sebuah URL. Ini adalah URL yang akan Anda gunakan di skrip bot Telegram.

## Menjalankan Bot Telegram

1.  **Dapatkan Token Bot**: Bicara dengan `@BotFather` di Telegram untuk membuat bot baru dan dapatkan token API-nya.
2.  **Buat file `.env`**: Di direktori yang sama dengan `bot.py` (di komputer lokal Anda), buat file bernama `.env` dan isi dengan:
    ```
    TELEGRAM_BOT_TOKEN="TOKEN_ANDA_DARI_BOTFATHER"
    SATURN_CLOUD_API_URL="URL_DEPLOYMENT_SATURN_CLOUD_ANDA/generate"
    ```
3.  **Instal Dependensi Bot**:
    `pip install python-telegram-bot python-dotenv requests`
4.  **Jalankan Bot**:
    `python bot.py`

Bot Anda sekarang aktif dan siap menerima perintah `/generate`.
