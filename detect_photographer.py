import cv2
import mediapipe as mp
import os
import shutil
import argparse
from pathlib import Path

def detect_photographer(input_dir, output_dir, face_threshold=0.5, hand_threshold=0.5, model_selection=1, debug=False):
    """
    Detects faces or hands in images within the input directory and moves them to the output directory.
    """
    
    # Initialize MediaPipe solutions
    mp_face_detection = mp.solutions.face_detection
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize detectors
    with mp_face_detection.FaceDetection(model_selection=model_selection, min_detection_confidence=face_threshold) as face_detection, \
         mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=hand_threshold) as hands:

        # Iterate through files in the input directory
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and os.path.splitext(f)[1].lower() in image_extensions]
        
        print(f"Found {len(files)} images in {input_dir}")

        for filename in files:
            filepath = os.path.join(input_dir, filename)
            
            try:
                # Read image
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
                debug_image = image.copy() if debug else None

                # 1. Detect Faces
                face_results = face_detection.process(image_rgb)
                if face_results.detections:
                    print(f"[Face Detected] {filename}")
                    detected = True
                    if debug:
                        for detection in face_results.detections:
                            mp_drawing.draw_detection(debug_image, detection)

                # 2. Detect Hands
                # Check hands even if face is detected to draw all detections in debug mode
                hand_results = hands.process(image_rgb)
                if hand_results.multi_hand_landmarks:
                    # If face was not detected, this counts as a detection
                    if not detected:
                        print(f"[Hand Detected] {filename}")
                        detected = True
                    
                    if debug:
                        for hand_landmarks in hand_results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(debug_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if detected:
                    output_path = os.path.join(output_dir, filename)
                    
                    if debug:
                        # Save debug image with annotations
                        debug_filename = f"debug_{filename}"
                        debug_path = os.path.join(output_dir, debug_filename)
                        # Encode with numpy to handle non-ASCII paths
                        is_success, buffer = cv2.imencode(os.path.splitext(filename)[1], debug_image)
                        if is_success:
                            with open(debug_path, "wb") as f:
                                f.write(buffer)
                        print(f"Debug image saved: {debug_path}")
                    
                    # Move original file
                    shutil.move(filepath, output_path)
                    print(f"Moved to: {output_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract images containing faces or hands.")
    parser.add_argument("input_dir", help="Path to the folder containing images.")
    parser.add_argument("output_dir", help="Path to the folder to save extracted images.")
    parser.add_argument("--face_threshold", type=float, default=0.5, help="Face detection confidence threshold (default: 0.5)")
    parser.add_argument("--hand_threshold", type=float, default=0.5, help="Hand detection confidence threshold (default: 0.5)")
    parser.add_argument("--model_selection", type=int, default=1, help="Face detection model selection: 0 (short-range) or 1 (full-range) (default: 1)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode to save annotated images.")

    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
    else:
        detect_photographer(args.input_dir, args.output_dir, 
                            face_threshold=args.face_threshold, 
                            hand_threshold=args.hand_threshold, 
                            model_selection=args.model_selection, 
                            debug=args.debug)
