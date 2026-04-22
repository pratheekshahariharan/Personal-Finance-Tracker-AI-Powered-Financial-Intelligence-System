import easyocr
import re
import numpy as np
import cv2

# Initialize reader globally to avoid reloading on every request
# Using 'en' for English
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        # gpu=False for better compatibility on CPU-only machines
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader

def extract_receipt_data(image_bytes):
    """
    Parses receipt image using EasyOCR and extracts Amount and Vendor.
    """
    # 1. Convert bytes to OpenCV image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"amount": 0.0, "description": "Failed to decode image"}
    
    # 2. Optimize image for OCR (Resizing)
    h, w = img.shape[:2]
    max_dim = 1024
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    # 3. Perform OCR
    reader = get_reader()
    results = reader.readtext(img)
    
    # results is a list of [bbox, text, confidence]
    full_text_lines = [r[1] for r in results]
    
    # 3. Extract Vendor (usually top 2 lines)
    vendor = "Unknown Vendor"
    if len(full_text_lines) > 0:
        vendor = full_text_lines[0]
        # Clean up vendor name
        vendor = re.sub(r'[^a-zA-Z0-9\s]', '', vendor).strip()

    # 4. Extract Amount
    # Look for the last number that looks like a total
    amount = 0.0
    
    # Pattern for currency-like numbers
    price_pattern = re.compile(r'(\d+[\.,]\s?\d{2})')
    
    # Iterate backwards to find the Total
    found_total = False
    for i in range(len(full_text_lines) - 1, -1, -1):
        line = full_text_lines[i].lower()
        
        # Check for keywords
        if any(kw in line for kw in ["total", "net", "amount", "payable", "sum"]):
            # Look in this line and the next line for a price
            search_text = line
            if i + 1 < len(full_text_lines):
                search_text += " " + full_text_lines[i+1]
            
            match = price_pattern.search(search_text)
            if match:
                price_str = match.group(1).replace(",", ".").replace(" ", "")
                try:
                    amount = float(price_str)
                    found_total = True
                    break
                except:
                    continue

    # Fallback: just find the largest number in the bottom half of the receipt
    if not found_total:
        all_numbers = []
        for r in results:
            text = r[1].replace(",", ".").replace(" ", "")
            match = re.search(r'(\d+\.\d{2})', text)
            if match:
                all_numbers.append(float(match.group(1)))
            else:
                # Try simple integers too
                match = re.search(r'^\d{2,5}$', text)
                if match:
                    all_numbers.append(float(match.group(0)))
        
        if all_numbers:
            amount = max(all_numbers)

    return {
        "amount": amount,
        "description": vendor,
        "raw_text": " | ".join(full_text_lines[:10]) # For debugging
    }
