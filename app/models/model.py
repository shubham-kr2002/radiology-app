import torch
import timm
from torchvision import transforms
from PIL import Image
import logging

# Configure logging (good practice for production)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Device configuration (use GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load pre-trained model (CheXNet-based) - Moved outside the function for efficiency
try:
    model = timm.create_model("densenet121", pretrained=True).to(device) # Load directly to device
    model.eval()  # Set model to evaluation mode
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise  # Re-raise the exception to stop execution if model loading fails

# Define image preprocessing - Moved outside for efficiency
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_xray(image_path):
    try:
        # Load and preprocess image
        try: # Nested try block for image loading errors
            image = Image.open(image_path).convert("RGB")
        except FileNotFoundError:
            logger.error(f"Image not found: {image_path}")
            return {"error": "Image not found"}
        except Exception as e: # Catch other image opening errors
            logger.error(f"Error opening image: {e}")
            return {"error": "Error opening image"}

        image = preprocess(image).unsqueeze(0).to(device)  # Add batch dimension and move to device

        # Perform inference
        with torch.no_grad():
            output = model(image)

        # Post-processing (Example: Get probabilities and predicted class)
        probabilities = torch.nn.functional.softmax(output, dim=1)  # Softmax for probabilities
        predicted_class = torch.argmax(probabilities).item()

        # Simulate a report (Replace with actual diagnosis logic)
        # Example using probabilities:
        pneumonia_prob = probabilities[0, 1].item()  # Assuming class 1 is pneumonia
        report = f"AI Analysis: Probability of Pneumonia: {pneumonia_prob:.4f}"

        logger.info(f"Inference complete for {image_path}") # Log successful inference

        return {"diagnosis": report, "probabilities": probabilities.tolist(), "predicted_class": predicted_class} # Include probabilities and class in response

    except Exception as e:
        logger.exception(f"Model inference failed: {e}") # Log the full traceback for debugging
        return {"error": "Model inference failed"} # More general error message for the user