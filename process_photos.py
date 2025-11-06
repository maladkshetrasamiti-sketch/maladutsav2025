#!/usr/bin/env python3
"""
fff
Process student photos for certificate printing:
- Detect faces in each photo
- Crop to passport size proportion
- Center the face
- Set white background
- Maintain original filename
- Save to Photos/Processed folder
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

# Configuration
INPUT_FOLDER = "Photos"
OUTPUT_FOLDER = os.path.join("Photos", "Processed")
PASSPORT_WIDTH = 413  # 35mm at 300 DPI
PASSPORT_HEIGHT = 531  # 45mm at 300 DPI
FACE_PERCENT = 0.6   # Face should take up about 60% of the height

def create_dirs():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def add_stationery_border(image):
    """Replace the floral border with a school-stationery / books themed border.

    The function keeps the same name to avoid changing other calls. It draws a
    warm paper-like background, a notebook-left margin, faint ruled lines,
    punched-hole markers, and small book/pencil-style icons in the corners.
    """
    if not isinstance(image, Image.Image):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    border_width = 28
    new_size = (image.width + 2 * border_width, image.height + 2 * border_width)

    # Paper-tinted background (soft warm white)
    paper_color = (255, 250, 240)
    bordered = Image.new('RGB', new_size, paper_color)
    bordered.paste(image, (border_width, border_width))

    draw = ImageDraw.Draw(bordered)

    # Draw a subtle paper top strip (like a header label)
    header_h = int(border_width * 0.9)
    header_box = [border_width, border_width - header_h, new_size[0] - border_width, border_width]
    draw.rectangle(header_box, fill=(249, 241, 228))

    # Notebook left margin (red) and faint vertical guide (blue)
    left_margin_x = border_width + 12
    draw.line([(left_margin_x, border_width), (left_margin_x, new_size[1] - border_width)], fill=(231, 76, 60), width=2)
    guide_x = left_margin_x + 8
    draw.line([(guide_x, border_width), (guide_x, new_size[1] - border_width)], fill=(189, 195, 199), width=1)

    # Ruled horizontal lines across the whole bordered area (faint blue)
    line_color = (214, 234, 248)
    spacing = 24
    for y in range(border_width + 8, new_size[1] - border_width, spacing):
        draw.line([(border_width + 6, y), (new_size[0] - border_width - 6, y)], fill=line_color, width=1)

    # Punch-hole markers on the left (three small circles)
    hole_r = 4
    hole_x = border_width - 6
    holes_y = [border_width + 40, new_size[1] // 2, new_size[1] - border_width - 40]
    for hy in holes_y:
        draw.ellipse([(hole_x - hole_r, hy - hole_r), (hole_x + hole_r, hy + hole_r)], fill=(240, 238, 235), outline=(200, 200, 200))

    # Small book icon (top-right)
    def draw_book(cx, cy, w=30, h=20):
        left = cx - w // 2
        top = cy - h // 2
        right = left + w
        bottom = top + h
        # book cover
        draw.rectangle([left, top, right, bottom], fill=(142, 68, 173), outline=(110, 44, 133))
        # spine
        spine_x = left + 6
        draw.line([(spine_x, top), (spine_x, bottom)], fill=(92, 40, 106), width=2)
        # pages (small white lines)
        for i in range(2):
            draw.line([(left + 8 + i*6, top + 4), (right - 6 + i*2, top + 4)], fill=(255, 240, 245), width=1)

    # Small pencil icon (bottom-right)
    def draw_pencil(cx, cy, scale=1.0):
        pw = int(28 * scale)
        ph = int(8 * scale)
        left = cx - pw // 2
        top = cy - ph // 2
        # pencil body
        draw.rectangle([left, top, left + pw, top + ph], fill=(243, 156, 18), outline=(200, 120, 10))
        # tip
        tip = [(left + pw, top), (left + pw + 6, top + ph // 2), (left + pw, top + ph)]
        draw.polygon(tip, fill=(149, 165, 166))

    draw_book(new_size[0] - border_width - 20, border_width + 16, w=34, h=22)
    draw_pencil(new_size[0] - border_width - 18, new_size[1] - border_width - 16, scale=1.0)

    # Light frame around the photo area to make it look like mounted on paper
    frame_box = [border_width - 2, border_width - 2, new_size[0] - border_width + 2, new_size[1] - border_width + 2]
    draw.rectangle(frame_box, outline=(220, 220, 220), width=2)

    # Slight smoothing and contrast so the stationery looks pleasant
    bordered = bordered.filter(ImageFilter.SMOOTH)
    enhancer = ImageEnhance.Contrast(bordered)
    bordered = enhancer.enhance(1.03)

    return bordered


def detect_face(image):
    """
    Detect faces in the image, including profile views.
    Returns the bounding box of the largest detected face.
    """
    # Load the cascades for both frontal and profile faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect frontal faces
    frontal_faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Detect profile faces
    profile_faces = profile_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Also try detecting profile faces in flipped image (opposite side profiles)
    flipped = cv2.flip(gray, 1)
    profile_faces_flipped = profile_cascade.detectMultiScale(
        flipped,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Adjust coordinates for flipped detections
    profile_faces_flipped = [(image.shape[1] - x - w, y, w, h) for (x, y, w, h) in profile_faces_flipped]
    
    # Combine all detections
    all_faces = list(frontal_faces) + list(profile_faces) + list(profile_faces_flipped)
    
    if not all_faces:
        return None
    
    # Get the largest face (in case multiple faces are detected)
    largest_face = max(all_faces, key=lambda rect: rect[2] * rect[3])
    return largest_face

def enhance_image_quality(img):
    """
    Enhance the image quality with smart adjustments.
    """
    # Convert to PIL Image if needed
    if not isinstance(img, Image.Image):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # Apply subtle sharpening
    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=3))
    
    # Enhance contrast slightly
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    # Adjust brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    # Enhance color
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.15)
    
    return img

def make_background_white(image):
    """Convert grayish backgrounds to pure white."""
    if not isinstance(image, Image.Image):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    mask = gray > 240  # near-white threshold
    img_array[mask] = [255, 255, 255]
    return Image.fromarray(img_array)


def process_image(input_path, output_path):
    """Process a single image to passport size format with quality enhancements."""
    try:
        # Read image
        img = cv2.imread(input_path)
        if img is None:
            print(f"⚠️ Could not read image: {input_path}")
            return False
        
        # Detect face
        face_rect = detect_face(img)
        if face_rect is None:
            print(f"⚠️ No face detected in: {input_path}")
            return False
            
        x, y, w, h = face_rect
        face_center = (x + w//2, y + h//2)
        
        # Calculate desired face size based on passport photo height
        desired_face_height = int(PASSPORT_HEIGHT * FACE_PERCENT)
        scale = desired_face_height / h
        
        # Calculate new dimensions
        new_width = int(img.shape[1] * scale)
        new_height = int(img.shape[0] * scale)
        
        # Resize image
        img_resized = cv2.resize(img, (new_width, new_height))
        
        # Calculate new face position after resize
        face_x = int(face_center[0] * scale)
        face_y = int(face_center[1] * scale)
        
        # Create white canvas of passport size
        canvas = np.full((PASSPORT_HEIGHT, PASSPORT_WIDTH, 3), 255, dtype=np.uint8)
        
        # Calculate placement position
        paste_x = PASSPORT_WIDTH//2 - face_x
        paste_y = PASSPORT_HEIGHT//2 - face_y
        
        # Create a mask for smooth blending
        mask = np.full((new_height, new_width), 255, dtype=np.uint8)
        
        # Place resized image onto white canvas
        for c in range(3):  # for each color channel
            for i in range(max(0, -paste_y), min(new_height, PASSPORT_HEIGHT - paste_y)):
                for j in range(max(0, -paste_x), min(new_width, PASSPORT_WIDTH - paste_x)):
                    if 0 <= paste_y + i < PASSPORT_HEIGHT and 0 <= paste_x + j < PASSPORT_WIDTH:
                        canvas[paste_y + i, paste_x + j, c] = img_resized[i, j, c]
        
        # Convert to PIL Image for saving (ensures proper color handling)
        pil_image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        
        # Enhance image quality
        # pil_image = enhance_image_quality(pil_image)
        pil_image = make_background_white(pil_image)

        # Add the stationery/books themed border
        pil_image = add_stationery_border(pil_image)

        # Save the final image
        pil_image.save(output_path, quality=95)

        print(f"✓ Processed: {os.path.basename(input_path)}")
        return True
        
    except Exception as e:
        print(f"⚠️ Error processing {input_path}: {str(e)}")
        return False

def main():
    """Process all images in the input folder."""
    create_dirs()
    
    success_count = 0
    error_count = 0
    
    # Process each file in the input directory
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            
            if process_image(input_path, output_path):
                success_count += 1
            else:
                error_count += 1
    
    # Print summary
    total = success_count + error_count
    if total > 0:
        print(f"\nProcessing complete:")
        print(f"✓ Successfully processed: {success_count}/{total} images")
        if error_count > 0:
            print(f"⚠️ Failed to process: {error_count}/{total} images")
        print(f"\nProcessed images saved to: {OUTPUT_FOLDER}/")
    else:
        print(f"\nNo image files found in {INPUT_FOLDER}/")

if __name__ == '__main__':
    main()