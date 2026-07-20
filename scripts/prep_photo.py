import sys
import os
import cv2
import numpy as np
from PIL import Image

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")

def prep_photo(photo_path):
    if not os.path.exists(photo_path):
        print(f"Error: {photo_path} does not exist.")
        return False

    print(f"Preprocessing {photo_path}...")
    
    # Try background removal with rembg
    try:
        from rembg import remove
        input_img = Image.open(photo_path)
        nobg_img = remove(input_img)
        img_np = np.array(nobg_img)
    except Exception as e:
        print(f"Warning: rembg failed or not installed ({e}). Falling back to OpenCV grayscale.")
        img_pil = Image.open(photo_path).convert("RGB")
        img_np = np.array(img_pil)

    # Convert to grayscale
    if len(img_np.shape) == 3 and img_np.shape[2] == 4:
        # Has alpha channel
        alpha = img_np[:, :, 3]
        gray = cv2.cvtColor(img_np[:, :, :3], cv2.COLOR_RGB2GRAY)
        # Composite onto white background
        white_bg = np.ones_like(gray) * 255
        gray = np.where(alpha > 50, gray, white_bg)
    elif len(img_np.shape) == 3:
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_np

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Save output
    cv2.imwrite(OUTPUT_PATH, enhanced)
    print(f"Prepped photo saved to {OUTPUT_PATH}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prep_photo(sys.argv[1])
    else:
        print("Usage: python scripts/prep_photo.py <path_to_source_photo.jpg>")
