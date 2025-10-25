#!/usr/bin/env python3
"""
Test landmark detection to see what's happening
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from landmark_detector import FaceLandmarkDetector
import cv2

print("=" * 60)
print("🔍 LANDMARK DETECTION TEST")
print("=" * 60)
print("\nThis will show you:")
print("1. If MediaPipe can detect your face")
print("2. How many landmarks are found")
print("3. Visual feedback with green dots on your face")
print("\nPress 'q' to quit")
print("=" * 60)

# Initialize detector
detector = FaceLandmarkDetector(static_image_mode=False)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit(1)

print("\n✅ Camera ready!")
print("Looking for faces...\n")

frame_count = 0
detected_count = 0
failed_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # Detect landmarks
    landmarks = detector.detect(frame)
    
    # Draw on frame
    display = frame.copy()
    h, w = display.shape[:2]
    
    if landmarks is not None:
        detected_count += 1
        
        # Draw landmarks
        annotated = detector.draw_landmarks(frame, landmarks)
        
        # Success message
        cv2.putText(annotated, f"FACE DETECTED! ({len(landmarks)} landmarks)", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(annotated, f"Detection rate: {detected_count}/{frame_count}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        display = annotated
        
        if detected_count == 1:
            print(f"✅ FACE DETECTED! Found {len(landmarks)} landmarks")
    else:
        failed_count += 1
        
        # No face message
        cv2.putText(display, "NO FACE DETECTED", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(display, "Please face the camera", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(display, f"Failed frames: {failed_count}/{frame_count}", 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 100), 1)
        
        if failed_count % 30 == 0:
            print(f"⚠️  Still no face detected... ({failed_count} frames)")
    
    cv2.putText(display, "Press Q to quit", 
               (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    cv2.imshow('Landmark Detection Test', display)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if frame_count >= 300:  # Auto-quit after 10 seconds
        break

cap.release()
cv2.destroyAllWindows()
detector.close()

print("\n" + "=" * 60)
print("📊 TEST RESULTS")
print("=" * 60)
print(f"Total frames: {frame_count}")
print(f"Faces detected: {detected_count}")
print(f"Failed detections: {failed_count}")
print(f"Success rate: {(detected_count/frame_count*100):.1f}%")

if detected_count == 0:
    print("\n❌ PROBLEM: MediaPipe couldn't detect any faces!")
    print("\nPossible reasons:")
    print("  1. Face not visible to camera")
    print("  2. Too dark (turn on lights)")
    print("  3. Face too close or too far (try 0.5-1m distance)")
    print("  4. Extreme angle (face camera directly)")
    print("  5. MediaPipe installation issue")
elif detected_count < frame_count * 0.5:
    print(f"\n⚠️  WARNING: Low detection rate ({detected_count/frame_count*100:.1f}%)")
    print("  Try improving lighting and facing camera directly")
else:
    print("\n✅ SUCCESS! MediaPipe is detecting your face correctly!")
    print("\nYou can now run the full demo:")
    print("  python demo_simple.py")

print("=" * 60)




