from PIL import Image
import numpy as np

# Disable PIL decompression bomb protection (REQUIRED for large images)
Image.MAX_IMAGE_PIXELS = None

def load_image(path):
    """
    Loads very large image safely for academic processing.
    """
    img = Image.open(path)
    img = img.convert("RGB")
    return np.asarray(img, dtype=np.uint8)

def save_image(path, array):
    Image.fromarray(array.astype(np.uint8)).save(path)
