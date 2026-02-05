from utils.image_io import load_image, save_image
from encoder.jpeg_encoder import encode_jpeg
from utils.logger import log_stage
from decoder.jpeg_decoder import decode_jpeg

INPUT = "data/input/input_image.jpg"
COMPRESSED = "data/output/compressed.jpg"
RECON = "data/output/reconstructed.png"

if __name__ == "__main__":
    img = load_image(INPUT)

    log_stage(
        "Image Loaded",
        before="No image in memory",
        after=f"Image shape: {img.shape}, dtype: {img.dtype}",
        next_step="Image will be padded and split into 8x8 blocks"
    )

    print("Encoding...")
    encode_jpeg(img, COMPRESSED)

    print("Decoding...")
    reconstructed = decode_jpeg(COMPRESSED)
    save_image(RECON, reconstructed)

    print("Decoding complete. Output saved.")