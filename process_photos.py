#!/usr/bin/env python3
"""
process_photos.py

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
    """Add a simple black-lined border around the photo.

    The photo is pasted unchanged and a clean black border is drawn in the
    margins so the original image content is preserved.
    """
    if not isinstance(image, Image.Image):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    border_width = 12
    new_size = (image.width + 2 * border_width, image.height + 2 * border_width)

    # Plain white background for the border area
    bordered = Image.new('RGB', new_size, (255, 255, 255))
    bordered.paste(image, (border_width, border_width))

    draw = ImageDraw.Draw(bordered)

    # Outer black rectangle (just outside the photo area)
    outer_box = [border_width - 2, border_width - 2, new_size[0] - border_width + 1, new_size[1] - border_width + 1]
    draw.rectangle(outer_box, outline=(0, 0, 0), width=3)

    # Thin inner line for subtle double-line border
    inner_box = [border_width + 4, border_width + 4, new_size[0] - border_width - 5, new_size[1] - border_width - 5]
    draw.rectangle(inner_box, outline=(0, 0, 0), width=1)

    return bordered

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