from multiprocessing import Pool, cpu_count
from encoder.block import pad_image_rgb, rgb_blocks
from encoder.worker import process_block
from encoder.rlc import rlc_encode
from encoder.huffman_encode import encode_dc, encode_ac
from bitstream.writer import BitWriter
from bitstream.headers import write_app0, write_dqt, write_sof0, write_dht, write_sos
from bitstream.markers import SOI, EOI
from encoder.quantization import Q_LUMA
import time
from utils.logger import log_stage


def encode_jpeg(image, output_path):
    # Pad image
    image = pad_image_rgb(image)
    height, width, _ = image.shape

    total_blocks = (height // 8) * (width // 8)

    bw = BitWriter()
    prev_dc = 0
    
    image = pad_image_rgb(image)
    height, width, _ = image.shape

    log_stage(
        "Padding & Block Formation",
        before="Original image dimensions",
        after=f"Padded image shape: {image.shape} (multiples of 8)",
        next_step="Image will be processed block-by-block (8x8)"
    )


    # -------- MULTIPROCESSING SETUP --------
    num_workers = cpu_count()
    chunk_size = 100   # very important for speed

    print(f"Using {num_workers} CPU cores")
    print(f"Total blocks: {total_blocks}")

    start_time = time.time()
    processed = 0
    log_interval = 5000

    with Pool(processes=num_workers) as pool:
        results = pool.imap(
            process_block,
            rgb_blocks(image),
            chunksize=chunk_size
        )

        # -------- SEQUENTIAL ENTROPY CODING --------
        for dc, ac in results:
            dc_diff = dc - prev_dc
            prev_dc = dc

            bw.write_bits(encode_dc(dc_diff))
            bw.write_bits(encode_ac(rlc_encode(ac)))

            processed += 1

            if processed % log_interval == 0:
                percent = (processed / total_blocks) * 100
                elapsed = time.time() - start_time
                speed = processed / elapsed
                remaining = (total_blocks - processed) / speed

                print(
                    f"{percent:.2f}% | "
                    f"{speed:.1f} blocks/s | "
                    f"ETA: {remaining/60:.1f} min",
                    flush=True
                )
                
    image = pad_image_rgb(image)
    height, width, _ = image.shape

    log_stage(
        "JPEG File Construction",
        before="Compressed bitstream in memory",
        after="JPEG markers + entropy data written",
        next_step="Final output is a valid .jpg file"
    )


    bw.flush()
    entropy = bw.get_bytes()

    # -------- WRITE JPEG FILE --------
    with open(output_path, "wb") as f:
        f.write(SOI)
        f.write(write_app0())
        f.write(write_dqt(Q_LUMA))
        f.write(write_sof0(height, width))
        f.write(write_dht())
        f.write(write_sos())
        f.write(entropy)
        f.write(EOI)
