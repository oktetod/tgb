import os
from huggingface_hub import hf_hub_download

# Pastikan direktori model ada
os.makedirs("models/Juggernaut-XL", exist_ok=True)
os.makedirs("models/ControlNet-XL", exist_ok=True)
os.makedirs("models/LoRA", exist_ok=True)
os.makedirs("models/VAE", exist_ok=True) # Untuk VAE jika diperlukan

print("Memulai mengunduh model...")

# 1. Unduh Model Utama: Juggernaut-XL V9
print("Mengunduh Juggernaut-XL v9...")
hf_hub_download(
    repo_id="RunDiffusion/Juggernaut-XL-v9",
    filename="Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
    local_dir="models/Juggernaut-XL",
    local_dir_use_symlinks=False
)
print("Selesai mengunduh Juggernaut-XL v9.")

# 2. Unduh Model ControlNet XL (contoh: Canny)
print("Mengunduh ControlNet-XL Canny...")
hf_hub_download(
    repo_id="diffusers/controlnet-canny-sdxl-1.0",
    filename="diffusion_pytorch_model.safetensors",
    local_dir="models/ControlNet-XL/canny",
    local_dir_use_symlinks=False
)
print("Selesai mengunduh ControlNet-XL Canny.")

# 3. Unduh Model ControlNet XL lain (contoh: Depth)
print("Mengunduh ControlNet-XL Depth...")
hf_hub_download(
    repo_id="diffusers/controlnet-depth-sdxl-1.0",
    filename="diffusion_pytorch_model.safetensors",
    local_dir="models/ControlNet-XL/depth",
    local_dir_use_symlinks=False
)
print("Selesai mengunduh ControlNet-XL Depth.")


# 4. Unduh LoRA (contoh: Detail Enhancer)
print("Mengunduh LoRA Detail Enhancer...")
hf_hub_download(
    repo_id="ostris/detail-tweaker-xl",
    filename="add-detail-xl.safetensors",
    local_dir="models/LoRA",
    local_dir_use_symlinks=False
)
print("Selesai mengunduh LoRA.")

# Anda bisa menambahkan model lain (v1, v2, dll) dengan cara yang sama.
# Cukup salin blok hf_hub_download dan ganti repo_id serta filename.

print("Semua model berhasil diunduh.")
