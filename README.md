# Steganography vs Modern Messaging Platforms

This project demonstrates how hidden data behaves when images are processed by modern platforms such as WhatsApp.

---

## 🧠 Overview

Steganography is the practice of hiding information inside other files — most commonly images — without changing their visible appearance.

However, modern messaging platforms often transform images during transmission.

This project explores what happens to hidden data under these conditions.

---

## 🧪 Experiment

The experiment follows a simple flow:

1. A message is stored in a file (`payload/secret.txt`)
2. The message is embedded into an image using steganography
3. The image is sent via WhatsApp in two ways:
   - as a regular image
   - as a document (file attachment)
4. The resulting files are analyzed and compared

---

## 🔐 Payload

The hidden message used in this experiment is stored in:
```bash
payload/secret.txt
```

Example content:
```bash
This is a hidden message.
If you are reading this, the steganography worked.
```

You can create it manually:

```bash
mkdir -p payload
echo "CONFIDENTIAL DATA - STEGANOGRAPHY TEST" > payload/secret.txt
```

🧬 Embedding the Data

Use steghide to embed the payload into the image:
```bash
steghide embed -cf images/original.jpg -ef payload/secret.txt
```

This will prompt for a passphrase.

📲 WhatsApp Test

Send the same image in two ways:

🔴 As Image
- Sent via gallery
- Automatically recompressed by WhatsApp

🟢 As Document
- Sent as file attachment
- Preserves original file structure

Save the received files as:
```bash
images/whatsapp.jpg
images/document.jpg
```

📊 Analysis

The script compares:
- Original image
- WhatsApp processed image
- Document version (unaltered)

It evaluates:
- Pixel differences
- Color distribution (RGB histograms)
- Entropy (information density)
- File size

📁 Project Structure
```bash
steganography-analysis/
├── advanced_analysis.py
├── images/
│   ├── original.jpg
│   ├── whatsapp.jpg
│   └── document.jpg
├── payload/
│   └── secret.txt
├── outputs/
│   └── analysis_result.png
├── requirements.txt
└── README.md
```

⚙️ Setup

Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

▶️ Run
```bash
python advanced_analysis.py
```

📈 Output

This folder is created automatically during execution.

The generated files include:
- Image comparison
- Pixel difference visualization
- RGB histograms
- Entropy and file size metrics

🔍 Expected Results
- The document version remains nearly identical to the original
- The WhatsApp image shows structural differences
- Hidden data is destroyed when the image is recompressed
- Hidden data survives when the file is sent as a document

🎯 Key Insight

Hidden data is not detected.

It is destroyed by transformation.

Modern systems do not need to identify hidden information —
they simply change the medium in a way that makes it disappear.

⚠️ Notes
- Image dimensions may change after WhatsApp processing
- Differences are often invisible to the human eye
- Analysis reveals structural changes at pixel level

🚀 Future Improvements
- Test compression-resistant steganography techniques
- Analyze frequency-domain embedding (DCT-based methods)
- Integrate automated experiment pipeline
- Extend analysis with LSB visualization

📄 License

This project is for educational and research purposes.