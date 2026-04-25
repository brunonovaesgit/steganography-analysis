import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "outputs"

images = {
    "Original": "images/original.jpg",
    "WhatsApp": "images/whatsapp.jpg",
    "Document": "images/document.jpg",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)


def validate_required_files(required_files):
    missing_files = [
        path for path in required_files.values()
        if not os.path.exists(path)
    ]

    if not missing_files:
        return

    print("\nMissing required image files:\n")

    for path in missing_files:
        print(f"  - {path}")

    print(
        "\nBefore running this analysis, make sure you have:\n"
        "  1. images/original.jpg  -> the original image with hidden data\n"
        "  2. images/whatsapp.jpg  -> the image sent and downloaded via WhatsApp as media\n"
        "  3. images/document.jpg  -> the same image sent and downloaded as a document\n\n"
        "Example workflow:\n"
        "  mkdir -p images payload outputs\n"
        "  cp /path/to/your/image.jpg images/original.jpg\n"
        "  echo 'CONFIDENTIAL DATA - STEGANOGRAPHY TEST' > payload/secret.txt\n"
        "  steghide embed -cf images/original.jpg -ef payload/secret.txt\n\n"
        "Then send images/original.jpg through WhatsApp twice:\n"
        "  - once as a regular image, save it as images/whatsapp.jpg\n"
        "  - once as a document, save it as images/document.jpg\n"
    )

    sys.exit(1)


validate_required_files(images)

def calculate_entropy(image):
    """
    Calculate Shannon entropy of the image.
    Higher entropy = more randomness/information.
    """
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    histogram_norm = histogram.ravel() / histogram.sum()
    histogram_norm = histogram_norm[histogram_norm > 0]
    return -np.sum(histogram_norm * np.log2(histogram_norm))


def file_size_kb(path):
    """Return file size in KB."""
    return os.path.getsize(path) / 1024


def safe_difference(img1, img2):
    """
    Compute pixel difference safely.
    If images have different sizes, resize to smallest common resolution.
    """
    if img1 is None or img2 is None:
        raise ValueError("One of the images could not be loaded. Check file paths.")

    height = min(img1.shape[0], img2.shape[0])
    width = min(img1.shape[1], img2.shape[1])

    img1_resized = cv2.resize(img1, (width, height))
    img2_resized = cv2.resize(img2, (width, height))

    return cv2.absdiff(img1_resized, img2_resized)


# Load and process images
data = {}

for name, path in images.items():
    image = cv2.imread(path)

    if image is None:
        raise ValueError(f"Failed to load image: {path}")

    data[name] = {
        "image": image,
        "entropy": calculate_entropy(image),
        "size": file_size_kb(path)
    }

# Compute differences
diff_whatsapp = safe_difference(data["Original"]["image"], data["WhatsApp"]["image"])
diff_document = safe_difference(data["Original"]["image"], data["Document"]["image"])

# Normalize difference for better visualization
diff_whatsapp_vis = cv2.normalize(diff_whatsapp, None, 0, 255, cv2.NORM_MINMAX)
diff_document_vis = cv2.normalize(diff_document, None, 0, 255, cv2.NORM_MINMAX)

# Plot everything
plt.figure(figsize=(16, 12))

# Original images
for i, (name, info) in enumerate(data.items()):
    plt.subplot(3, 3, i + 1)
    plt.imshow(cv2.cvtColor(info["image"], cv2.COLOR_BGR2RGB))
    plt.title(name)
    plt.axis("off")

# Differences
plt.subplot(3, 3, 4)
plt.imshow(diff_whatsapp_vis)
plt.title("Original vs WhatsApp (Difference)")
plt.axis("off")

plt.subplot(3, 3, 5)
plt.imshow(diff_document_vis)
plt.title("Original vs Document (Difference)")
plt.axis("off")

# Histograms
for i, (name, info) in enumerate(data.items()):
    plt.subplot(3, 3, 7 + i)

    for channel, color in enumerate(["b", "g", "r"]):
        hist = cv2.calcHist([info["image"]], [channel], None, [256], [0, 256])
        plt.plot(hist, color=color)

    plt.title(f"Histogram - {name}")

plt.tight_layout()
plt.savefig("outputs/analysis_result.png")

# Console summary
print("\n=== ANALYSIS SUMMARY ===\n")

for name, info in data.items():
    print(f"{name}:")
    print(f"  File size: {info['size']:.2f} KB")
    print(f"  Entropy:   {info['entropy']:.4f}")
    print()