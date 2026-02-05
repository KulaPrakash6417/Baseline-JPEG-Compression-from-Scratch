# **Baseline JPEG Compression from Scratch**

### *End-to-End Encoder and Decoder Implementation*

---

## **1. Introduction**

Digital images consume a large amount of storage, especially when stored in raw or lossless formats. Image compression techniques aim to reduce storage requirements while preserving perceptual quality. One of the most widely used image compression standards is **JPEG**, which achieves high compression ratios using transform coding, quantization, and entropy coding.

The objective of this project is to **design and implement a baseline JPEG compression system entirely from scratch**, without using any built-in JPEG encoder or decoder libraries. The system takes a large raw image (≥100 MB), compresses it using JPEG principles, and produces a valid `.jpg` file that can be opened by standard image viewers.

This project focuses not only on correctness, but also on **scalability, performance, and adherence to the JPEG standard (ITU-T T.81)**.

---

## **2. Problem Statement**

Design and implement a baseline JPEG encoder and decoder that:

* Accepts a large input image (≥100 MB)
* Compresses the image using JPEG techniques
* Produces a valid `.jpg` file
* Does **not** use any JPEG compression libraries
* Implements all major algorithmic steps manually
* Includes entropy coding and a JPEG-compliant file structure

---

## **3. High-Level JPEG Pipeline**

The JPEG compression pipeline implemented in this project is shown below:

```
                                      RGB Image
                                           ↓
                              Block-wise RGB → Y conversion
                                           ↓
                                  Level shifting (−128)
                                           ↓
                                  8×8 Block Formation
                                           ↓
                                        2-D DCT
                                           ↓
                                      Quantization
                                           ↓
                                      Zigzag Scan
                                           ↓
                             DC DPCM + AC Run-Length Coding
                                           ↓
                                    Huffman Encoding
                                           ↓
                                  JPEG Bitstream (.jpg)
```

Each stage is explained in detail in the following sections.

---

## **4. Image Preprocessing**

### **4.1 RGB to Y Conversion**

JPEG compression is applied primarily to the **luminance (Y)** channel because the human visual system is more sensitive to brightness than color.

For each 8×8 RGB block, the Y channel is computed using: Y = 0.299R + 0.587G + 0.114B

To avoid excessive memory usage for large images, this conversion is performed **block-by-block**, not on the full image.

### **4.2 Level Shifting**

Pixel values in the range `[0, 255]` are shifted to `[-128, 127]`: Y_{shifted} = Y - 128

This centers values around zero, which improves DCT energy compaction.

---

## **5. Block Formation and Padding**

JPEG operates on **8×8 blocks**.

If the image dimensions are not multiples of 8:

* The image is padded by replicating border pixels
* Padding ensures no artificial edges are introduced

This step is necessary for correct block-based processing.

---

## **6. Discrete Cosine Transform (DCT)**

### **6.1 Purpose of the DCT**

The DCT converts spatial pixel values into frequency coefficients. Most natural images have:

* High energy in low frequencies
* Low energy in high frequencies

This allows effective compression after quantization.

---

### **6.2 Matrix-Based DCT Implementation**

Instead of a slow nested-loop DCT, the transform is implemented as: DCT = C * X * C^T

Where:
* (X) is the 8×8 input block
* (C) is the precomputed DCT basis matrix

This approach:

* Implements the exact JPEG DCT
* Uses NumPy’s optimized matrix multiplication
* Achieves a **10–20× speedup**

---

## **7. Quantization**

Quantization is the **only lossy step** in JPEG compression.

Each DCT coefficient is divided by a corresponding value from the **standard JPEG luminance quantization table**:

Q(u,v) = round({DCT(u,v)} / {QT(u,v)})

Higher-frequency coefficients are quantized more aggressively, leading to many zeros.

---

## **8. Zigzag Scanning**

Quantized coefficients are reordered in **zigzag order**, which:

* Places low-frequency coefficients first
* Groups long runs of zeros at the end

This improves the efficiency of run-length and Huffman coding.

---

## **9. Entropy Coding Preparation**

### **9.1 DC Differential Pulse Code Modulation (DPCM)**

The DC coefficient of each block is encoded as a difference from the previous block:
DC_{diff} = DC_i - DC_{i-1}

This reduces the entropy of DC values.

---

### **9.2 AC Run-Length Coding (RLC)**

AC coefficients are encoded as `(RUNLENGTH, SIZE)` pairs:

* `RUNLENGTH`: number of preceding zeros
* `SIZE`: magnitude category of the coefficient

Special symbols:

* **EOB (0,0)**: End of Block
* **ZRL (15,0)**: 16 consecutive zeros

---

## **10. Huffman Coding**

### **10.1 Canonical Huffman Tables**

Standard JPEG luminance Huffman tables (Annex K, ITU-T T.81) are used.

Rather than hardcoding bit patterns:

* Tables are generated from `BITS` and `HUFFVAL`
* Canonical Huffman codes are constructed programmatically

This ensures:

* Correctness
* Compatibility with JPEG decoders
* Consistency between encoding and headers

---

### **10.2 Bitstream Writing**

Entropy-coded bits are written using a custom `BitWriter` that:

* Writes bits MSB-first
* Applies byte stuffing (`0xFF → 0xFF00`)
* Ensures byte alignment before `EOI`

This is essential for generating a valid JPEG file.

---

## **11. JPEG File Structure**

The final output file strictly follows the JPEG baseline format:

| Marker       | Description             |
| ------------ | ----------------------- |
| SOI          | Start of Image          |
| APP0         | JFIF Header             |
| DQT          | Quantization Table      |
| SOF0         | Frame Header (Baseline) |
| DHT          | Huffman Tables          |
| SOS          | Start of Scan           |
| Entropy Data | Compressed Image        |
| EOI          | End of Image            |

Special care was taken to:

* Use correct segment lengths
* Match table IDs across headers
* Ensure byte-aligned entropy data

---

## **12. Parallelization and Performance Optimization**

### **12.1 Motivation**

A ≥200 MB image contains **millions of 8×8 blocks**. A naive implementation would take hours.

---

### **12.2 Parallel Design**

The pipeline was split into two stages:

#### **Parallel Stage**

* RGB → Y conversion
* DCT
* Quantization
* Zigzag scan

Each block is independent → ideal for multiprocessing.

#### **Sequential Stage**

* DC DPCM
* Huffman encoding
* Bitstream writing

These steps depend on block order and must remain serial.

---

### **12.3 Multiprocessing Implementation**

* Python `multiprocessing.Pool` used
* Work distributed across all CPU cores
* Chunking applied to reduce overhead

This resulted in a **significant speedup** while preserving JPEG correctness.

---

## **13. Experimental Results**

### **13.1 Compression Performance**

| Metric            | Value                 |
| ----------------- | --------------------- |
| Input Image Size  | ≥100 MB               |
| Output JPEG Size  | Significantly smaller |
| Compression Ratio | ~8× – 15×             |
| Output Format     | Valid `.jpg`          |

---

### **13.2 Visual Quality**

* Blocking artifacts visible at high compression
* Low-frequency content well preserved
* Results consistent with baseline JPEG behavior

---

## **14. Limitations**

* Only luminance channel compressed
* No chroma subsampling
* No progressive JPEG
* Decoder implemented separately for verification

---

## **15. Conclusion**
This project successfully demonstrates a **complete, scalable, and standards-compliant JPEG compression system implemented entirely from scratch**. The implementation handles very large images, applies correct entropy coding, produces valid JPEG files, and incorporates performance optimizations through parallel processing and matrix-based transforms.

The project closely follows the JPEG baseline specification and provides a deep understanding of how JPEG compression works internally.

---

## **16. References**

1. ITU-T Recommendation T.81 – JPEG Standard
2. Wallace, G.K., *The JPEG Still Picture Compression Standard*
3. Gonzalez & Woods, *Digital Image Processing*

# Baseline-JPEG-Compression-from-Scratch
