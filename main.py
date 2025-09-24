import torch
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from diffusers import StableDiffusionXLPipeline, ControlNetModel, AutoencoderKL
from diffusers.utils import load_image
from PIL import Image
import numpy as np
import uuid
import os
from pydantic import BaseModel
from typing import Optional

# Pastikan direktori output ada
os.makedirs("output", exist_ok=True)

# --- Konfigurasi dan Pemuatan Model ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

# Path ke model yang sudah diunduh
base_model_path = "models/Juggernaut-XL/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
controlnet_canny_path = "models/ControlNet-XL/canny/diffusion_pytorch_model.safetensors"
controlnet_depth_path = "models/ControlNet-XL/depth/diffusion_pytorch_model.safetensors"
lora_detail_path = "models/LoRA/add-detail-xl.safetensors"

# Inisialisasi ControlNet models
controlnet_canny = ControlNetModel.from_single_file(controlnet_canny_path, torch_dtype=DTYPE)
controlnet_depth = ControlNetModel.from_single_file(controlnet_depth_path, torch_dtype=DTYPE)

# Inisialisasi Pipeline Utama (tanpa ControlNet pada awalnya)
print("Memuat pipeline utama Juggernaut-XL...")
pipe = StableDiffusionXLPipeline.from_single_file(
    base_model_path,
    torch_dtype=DTYPE,
    variant="fp16",
    use_safetensors=True
)
pipe.to(DEVICE)
print("Pipeline utama berhasil dimuat.")

# Inisialisasi Aplikasi FastAPI
app = FastAPI()

# Definisikan model request body
class GenerationRequest(BaseModel):
    prompt: str
    negative_prompt: str = "worst quality, low quality, bad anatomy, deformed, ugly, disfigured"
    use_controlnet: Optional[str] = None  # "canny" atau "depth"
    use_lora: bool = False
    control_image_url: Optional[str] = None
    width: int = 1024
    height: int = 1024
    num_inference_steps: int = 30
    guidance_scale: float = 7.5

@app.get("/")
def read_root():
    return {"status": "API Juggernaut SDXL sedang berjalan"}

@app.post("/generate")
async def generate_image(request: GenerationRequest = Body(...)):
    prompt = request.prompt
    negative_prompt = request.negative_prompt
    
    current_pipe = pipe # Gunakan pipeline utama
    
    # --- Penanganan ControlNet ---
    if request.use_controlnet and request.control_image_url:
        print(f"Menggunakan ControlNet: {request.use_controlnet}")
        control_image = load_image(request.control_image_url).convert("RGB")
        
        selected_controlnet = None
        if request.use_controlnet == "canny":
            selected_controlnet = controlnet_canny
            # Preprocess image untuk Canny
            canny_image = np.array(control_image)
            canny_image = cv2.Canny(canny_image, 100, 200)
            canny_image = canny_image[:, :, None]
            canny_image = np.concatenate([canny_image, canny_image, canny_image], axis=2)
            control_image = Image.fromarray(canny_image)

        elif request.use_controlnet == "depth":
            selected_controlnet = controlnet_depth
            # (Anda mungkin perlu menambahkan preprocessor untuk depth di sini jika diperlukan)

        if selected_controlnet:
            # Buat pipeline baru dengan ControlNet
            current_pipe = StableDiffusionXLControlNetPipeline.from_single_file(
                base_model_path,
                controlnet=selected_controlnet,
                torch_dtype=DTYPE,
                variant="fp16"
            ).to(DEVICE)
            
    # --- Penanganan LoRA ---
    if request.use_lora:
        print("Mengaktifkan LoRA: Detail Enhancer")
        current_pipe.load_lora_weights(lora_detail_path)
        # Atur bobot LoRA jika perlu, contoh: prompt = f"{prompt} <lora:add-detail-xl:1.0>"
    
    print("Memulai proses generasi gambar...")
    generator = torch.Generator(device=DEVICE).manual_seed(0) # Gunakan seed untuk hasil yang konsisten
    
    # Argumen untuk pipeline
    kwargs = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": request.width,
        "height": request.height,
        "num_inference_steps": request.num_inference_steps,
        "guidance_scale": request.guidance_scale,
        "generator": generator
    }

    if request.use_controlnet and request.control_image_url:
        kwargs["image"] = control_image
        kwargs["controlnet_conditioning_scale"] = 0.5 # Sesuaikan nilai ini

    image = current_pipe(**kwargs).images[0]
    
    # --- Lepas LoRA setelah digunakan agar tidak mempengaruhi request lain ---
    if request.use_lora:
        current_pipe.unload_lora_weights()
        print("LoRA dinonaktifkan.")

    # Simpan gambar
    filename = f"output/{uuid.uuid4()}.png"
    image.save(filename)
    
    print(f"Gambar berhasil dibuat dan disimpan di {filename}")
    return FileResponse(filename)
