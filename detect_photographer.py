import cv2
import mediapipe as mp
import os
import shutil
import argparse
from pathlib import Path

def detect_photographer(input_dir, output_dir, confidence_threshold=0.5):
    """
    Detects faces or hands in images within the input directory and copies them to the output directory.
    """
    
    # Initialize MediaPipe solutions
    mp_face_detection = mp.solutions.face_detection
    mp_hands = mp.solutions.hands

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize detectors
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=confidence_threshold) as face_detection, \
         mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=confidence_threshold) as hands:

        # Iterate through files in the input directory
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and os.path.splitext(f)[1].lower() in image_extensions]
        
        print(f"Found {len(files)} images in {input_dir}")

        for filename in files:
            filepath = os.path.join(input_dir, filename)
            
            try:
                # Read image
                # Use cv2.imdecode to handle non-ASCII paths if necessary, but standard imread usually works on modern OS
                # For robustness with Japanese paths on Windows, numpy method is safer
                import numpy as np
                with open(filepath, 'rb') as f:
                    file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
                    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                if image is None:
                    print(f"Could not read image: {filename}")
                    continue

                # Convert the BGR image to RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                detected = False

                # 1. Detect Faces
                face_results = face_detection.process(image_rgb)
                if face_results.detections:
                    print(f"[Face Detected] {filename}")
                    detected = True

                # 2. Detect Hands (if no face detected yet, or check both)
                # Optimization: if face is already found, we can skip hands if we just want "any" detection.
                # But user might want to know WHAT was detected. For now, let's just copy if EITHER is found.
                if not detected:
                    hand_results = hands.process(image_rgb)
                    if hand_results.multi_hand_landmarks:
                        print(f"[Hand Detected] {filename}")
                        detected = True

                if detected:
                    output_path = os.path.join(output_dir, filename)
                    shutil.copy2(filepath, output_path)
                    print(f"Copied to: {output_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract images containing faces or hands.")
    parser.add_argument("input_dir", help="Path to the folder containing images.")
    parser.add_argument("output_dir", help="Path to the folder to save extracted images.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Detection confidence threshold (default: 0.5)")

    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
    else:
        detect_photographer(args.input_dir, args.output_dir, args.threshold)
