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
from typing import List, Optional
import json
from datetime import datetime
import asyncio
from models.cycle_gan_model import CycleGANModel

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
    allow_origins=["*"],  # In production, replace with specific origins
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

# In-memory database for demo purposes (would be Cassandra in production)
style_db = {
    "s1": {
        "id": "s1",
        "name": "Monochrome",
        "description": "Classic black and white style",
        "model_path": "backend/models/monochrome_cyclegan.pth"
    },
    "s2": {
        "id": "s2",
        "name": "Vintage",
        "description": "Retro-inspired warm tones",
        "model_path": "backend/models/vintage_cyclegan.pth"
    },
    "s3": {
        "id": "s3",
        "name": "Nature",
        "description": "Earthy green environment",
        "model_path": "backend/models/nature_cyclegan.pth"
    },
    "s4": {
        "id": "s4",
        "name": "Neon",
        "description": "Vibrant pink urban style",
        "model_path": "backend/models/neon_cyclegan.pth"
    }
}

# Request models
class StyleTransferRequest(BaseModel):
    product_id: str
    style_id: str
    
class StyleResponse(BaseModel):
    id: str
    name: str
    description: str

class ProductStyleResponse(BaseModel):
    id: str
    product_id: str
    style_id: str
    image_url: str
    created_at: str

# Load pretrained CycleGAN model
def load_model(style_id: str):
    try:
        # In a real implementation, we would load the actual model
        # For this demo, we'll simulate the model loading
        logger.info(f"Loading model for style {style_id}: {style_db[style_id]['name']}")
        
        # Create a dummy model for demonstration
        model = CycleGANModel()
        
        # In a real implementation, we would load weights like this:
        # model.load_state_dict(torch.load(style_db[style_id]['model_path']))
        
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

# Process image with CycleGAN
async def process_image(input_path: str, output_path: str, style_id: str):
    try:
        # Load the image
        img = Image.open(input_path).convert('RGB')
        
        # Preprocess the image
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        img_tensor = preprocess(img).unsqueeze(0)
        
        # Load the model
        model = load_model(style_id)
        
        # In a real implementation, we would run inference
        # For this demo, we'll simulate the style transfer
        logger.info(f"Applying style transfer with style {style_id}")
        await asyncio.sleep(2)  # Simulate processing time
        
        # For demo purposes, just save the original image
        # In a real implementation, we would save the transformed image
        img.save(output_path)
        
        logger.info(f"Style transfer complete, saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error in style transfer: {e}")
        return False

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to StyleShift API"}

@app.get("/api/styles", response_model=List[StyleResponse])
async def get_styles():
    return [
        {"id": style["id"], "name": style["name"], "description": style["description"]}
        for style in style_db.values()
    ]

@app.post("/api/transfer", response_model=ProductStyleResponse)
async def transfer_style(request: StyleTransferRequest, background_tasks: BackgroundTasks):
    try:
        # Generate unique ID for this transfer
        transfer_id = str(uuid.uuid4())
        
        # In a real implementation, we would get the product image from a database
        # For this demo, we'll use a placeholder path
        input_path = f"src/assets/products/{request.product_id}.jpg"
        
        # Create output path
        output_filename = f"{request.product_id}_{request.style_id}_{transfer_id}.jpg"
        output_path = f"backend/results/{output_filename}"
        
        # Process the image in the background
        background_tasks.add_task(process_image, input_path, output_path, request.style_id)
        
        # Return response with URL to the result
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

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)