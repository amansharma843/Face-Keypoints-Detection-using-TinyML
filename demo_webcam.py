#!/usr/bin/env python3
"""
🎥 Live Webcam Face Landmark Detection Demo

This demo shows real-time facial keypoint detection from your webcam.
It's the first step in our privacy-preserving face verification system.

Usage:
    python demo_webcam.py

Controls:
    - Press 'q' to quit
    - Press 's' to save snapshot
    - Press 'f' to extract and display features
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from landmark_detector import FaceLandmarkDetector
from geometric_features import GeometricFeatureExtractor
from hdc_encoder import HDCEncoder

import cv2
import numpy as np


def main():
    print("=" * 60)
    print("🎥 WEBCAM FACE LANDMARK DETECTION DEMO")
    print("=" * 60)
    print("\nThis demo detects 478 facial keypoints in real-time!")
    print("\nControls:")
    print("  'q' - Quit")
    print("  's' - Save snapshot")
    print("  'f' - Extract features")
    print("=" * 60)
    print("\nStarting webcam...")
    
    # Initialize components
    detector = FaceLandmarkDetector(static_image_mode=False)
    feature_extractor = GeometricFeatureExtractor()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        print("   Make sure no other application is using the camera")
        return
    
    print("✅ Webcam opened successfully!")
    
    snapshot_count = 0
    show_features = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame")
            break
        
        # Detect landmarks
        landmarks = detector.detect(frame)
        
        if landmarks is not None:
            # Draw landmarks
            annotated_frame = detector.draw_landmarks(frame, landmarks)
            
            # Extract features if requested
            if show_features:
                features = feature_extractor.get_feature_vector(landmarks)
                
                # Display feature stats
                y_offset = 30
                cv2.putText(annotated_frame, f"Features extracted: {len(features)}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                y_offset += 30
                cv2.putText(annotated_frame, f"Mean: {features.mean():.2f}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 25
                cv2.putText(annotated_frame, f"Std: {features.std():.2f}", 
                           (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                cv2.putText(annotated_frame, f"Landmarks detected: {len(landmarks)}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.putText(annotated_frame, "Press 'f' to show features", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            annotated_frame = frame.copy()
            cv2.putText(annotated_frame, "No face detected - please face the camera", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display
        cv2.imshow('Face Landmark Detection', annotated_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n👋 Quitting...")
            break
        elif key == ord('s') and landmarks is not None:
            # Save snapshot
            os.makedirs('results', exist_ok=True)
            filename = f"results/snapshot_{snapshot_count}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"📸 Saved: {filename}")
            snapshot_count += 1
        elif key == ord('f'):
            show_features = not show_features
            print(f"{'✅' if show_features else '❌'} Feature display: {'ON' if show_features else 'OFF'}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    print("✅ Demo finished!")


if __name__ == "__main__":
    main()

