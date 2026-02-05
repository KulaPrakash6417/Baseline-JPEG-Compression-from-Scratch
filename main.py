from utils.image_io import load_image
from encoder.jpeg_encoder import encode_jpeg
from utils.logger import log_stage

INPUT = "data/input/input_image.jpg"
OUTPUT = "data/output/compressed.jpg"

if __name__ == "__main__":
    img = load_image(INPUT)

    log_stage(
        "Image Loaded",
        before="No image in memory",
        after=f"Image shape: {img.shape}, dtype: {img.dtype}",
        next_step="Image will be padded and split into 8x8 blocks"
    )

    encode_jpeg(img, OUTPUT)
