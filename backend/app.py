from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
import os
import uuid
import logging
import uvicorn
from typing import List
from datetime import datetime
import asyncio

# Define CycleGAN Generator
class ResidualBlock(nn.Module):
    def __init__(self, in_features):
        super(ResidualBlock, self).__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_features, in_features, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(in_features),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_features, in_features, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(in_features)
        )
    
    def forward(self, x):
        return x + self.block(x)

class Generator(nn.Module):
    def __init__(self, input_nc=3, output_nc=3, n_residual_blocks=9):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(input_nc, 64, kernel_size=7, stride=1, padding=3, bias=False),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),
            *[ResidualBlock(64) for _ in range(n_residual_blocks)],
            nn.Conv2d(64, output_nc, kernel_size=7, stride=1, padding=3, bias=False),
            nn.Tanh()
        )
    
    def forward(self, x):
        return self.model(x)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="StyleShift API", 
              description="Style Transfer API for E-Commerce using CycleGAN",
              version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("backend/uploads", exist_ok=True)
os.makedirs("backend/results", exist_ok=True)
os.makedirs("backend/models", exist_ok=True)

# Mount static files directory
app.mount("/images", StaticFiles(directory="backend/results"), name="images")

# In-memory style database
style_db = {
    "s1": {"id": "s1", "name": "Monochrome", "model_path": "backend/models/monochrome_cyclegan.pth"},
    "s2": {"id": "s2", "name": "Vintage", "model_path": "backend/models/vintage_cyclegan.pth"},
    "s3": {"id": "s3", "name": "Nature", "model_path": "backend/models/nature_cyclegan.pth"},
    "s4": {"id": "s4", "name": "Neon", "model_path": "backend/models/neon_cyclegan.pth"},
}

# Request model
class StyleTransferRequest(BaseModel):
    product_id: str
    style_id: str

# Load CycleGAN generator model
def load_model(style_id: str):
    try:
        model = Generator()
        model.load_state_dict(torch.load(style_db[style_id]['model_path'], map_location=torch.device('cpu')))
        model.eval()
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

# Apply CycleGAN for style transfer
async def process_image(input_path: str, output_path: str, style_id: str):
    try:
        img = Image.open(input_path).convert('RGB')
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        img_tensor = transform(img).unsqueeze(0)
        
        model = load_model(style_id)
        with torch.no_grad():
            output_tensor = model(img_tensor)
        
        output_img = output_tensor.squeeze().detach().numpy()
        output_img = ((output_img + 1) / 2 * 255).astype('uint8')
        output_img = Image.fromarray(output_img.transpose(1, 2, 0))
        output_img.save(output_path)
        return True
    except Exception as e:
        logger.error(f"Error in style transfer: {e}")
        return False

# API Endpoints
@app.post("/api/transfer")
async def transfer_style(request: StyleTransferRequest, background_tasks: BackgroundTasks):
    try:
        transfer_id = str(uuid.uuid4())
        input_path = f"src/assets/products/{request.product_id}.jpg"
        output_filename = f"{request.product_id}_{request.style_id}_{transfer_id}.jpg"
        output_path = f"backend/results/{output_filename}"
        
        background_tasks.add_task(process_image, input_path, output_path, request.style_id)
        
        return {
            "id": transfer_id,
            "product_id": request.product_id,
            "style_id": request.style_id,
            "image_url": f"/images/{output_filename}",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in style transfer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
