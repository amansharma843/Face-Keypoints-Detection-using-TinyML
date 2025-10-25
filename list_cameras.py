#!/usr/bin/env python3
"""
List all available cameras and test them
"""

import cv2

print("=" * 60)
print("📹 AVAILABLE CAMERAS")
print("=" * 60)

available_cameras = []

# Try first 5 camera indices
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            available_cameras.append({
                'index': i,
                'resolution': f"{w}x{h}"
            })
            print(f"\n✅ Camera {i}:")
            print(f"   Resolution: {w}x{h}")
            
            # Try to identify camera type
            if i == 0 and w < 2000:
                print(f"   Type: Likely BUILT-IN MacBook camera")
            elif w >= 1920:
                print(f"   Type: Likely EXTERNAL/iPhone camera")
        cap.release()

if not available_cameras:
    print("\n❌ No cameras found!")
else:
    print(f"\n" + "=" * 60)
    print(f"Found {len(available_cameras)} camera(s)")
    print("=" * 60)
    
    if len(available_cameras) > 1:
        print("\n💡 TIP: You have multiple cameras!")
        print("   Camera 0 is usually the built-in MacBook camera")
        print("   Other cameras are external (iPhone, USB webcam, etc.)")

print("\n" + "=" * 60)




