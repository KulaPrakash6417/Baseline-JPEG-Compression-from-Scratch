import os

def compression_ratio(original_path, compressed_path):
    return os.path.getsize(original_path) / os.path.getsize(compressed_path)
