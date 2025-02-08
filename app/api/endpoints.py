from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
import io
import os
from app.model import predict_xray  # Import AI model function
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze/")
async def analyze_xray(file: UploadFile = File(...)):
    # Validate file type
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    filename, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in allowed_extensions:
        logger.warning(f"Invalid file type uploaded: {file.filename}") # Log the invalid file
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG and PNG allowed.")

    try:
        # Read and save image (using a temporary file)
        try:
            os.makedirs("uploaded_images", exist_ok=True)  # Create directory if needed

            # Use a temporary file to avoid potential issues with file locking
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False, dir="uploaded_images") as tmp:
                filepath = tmp.name
                contents = await file.read()
                image = Image.open(io.BytesIO(contents)).convert("L") # Convert and open in one go
                image.save(filepath)

            logger.info(f"Image saved to: {filepath}")

        except Exception as e:
            logger.error(f"Error saving uploaded image: {e}")
            raise HTTPException(status_code=500, detail="Error saving image")

        try:
            # Run AI model for diagnosis
            result = predict_xray(filepath)  # Call the prediction function

            # Log the result (important for auditing/monitoring)
            logger.info(f"AI analysis result: {result}")

            return {"filename": file.filename, "diagnosis": result}

        except Exception as e:  # Catch exceptions from model inference
            logger.exception(f"Error during AI analysis: {e}") # Log the full traceback
            raise HTTPException(status_code=500, detail="Error during AI analysis") # More general for the user

    except HTTPException as e: # Re-raise HTTPExceptions to maintain their status code
        raise # important to maintain the original HTTP error

    except Exception as e:  # Catch any other unexpected exceptions
        logger.exception(f"Unexpected error in /analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")