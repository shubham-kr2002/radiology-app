from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
import os

router = APIRouter()

@router.post("/upload/")
async def upload_xray(file: UploadFile = File(...)):
    # Check file extension
    allowed_extensions = [".jpg", ".jpeg", ".png"]  # Include .jpeg for common JPGs
    filename, ext = os.path.splitext(file.filename)
    ext = ext.lower()  # Handle case-insensitivity (.JPG, .jpg)

    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG and PNG files are allowed.")

    try:
        # Read the image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))


        # Convert to grayscale (simulate preprocessing)
        image = image.convert("L")

        # Create the directory if it doesn't exist
        os.makedirs("uploaded_images", exist_ok=True)  # Prevents errors if directory missing


        # Save the image
        filepath = os.path.join("uploaded_images", file.filename) # Use os.path.join for cross-platform paths
        image.save(filepath)

        return {"filename": file.filename, "message": "X-ray uploaded successfully"}

    except Exception as e: # Catch any potential errors during image processing
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")