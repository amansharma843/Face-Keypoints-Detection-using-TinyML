#!/usr/bin/env python3
"""
Simple camera test to verify webcam access
"""

import cv2

print("🎥 Testing camera access...")
print("Press 'q' to quit\n")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    print("\nTroubleshooting:")
    print("1. Check System Settings → Privacy & Security → Camera")
    print("2. Enable camera access for Terminal/Python")
    print("3. Close other apps using the camera (Zoom, FaceTime, etc.)")
    exit(1)

print("✅ Camera opened successfully!")
print("Reading frames...\n")

frame_count = 0
while frame_count < 10:
    ret, frame = cap.read()
    
    if not ret:
        print(f"❌ Error reading frame {frame_count + 1}")
        break
    
    frame_count += 1
    h, w = frame.shape[:2]
    print(f"✅ Frame {frame_count}: {w}x{h} pixels")
    
    cv2.putText(frame, f"Frame {frame_count}/10 - Press Q to quit", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('Camera Test', frame)
    
    if cv2.waitKey(100) & 0xFF == ord('q'):
        print("\n👋 Quit by user")
        break

cap.release()
cv2.destroyAllWindows()

if frame_count >= 10:
    print(f"\n✅ Camera test PASSED! ({frame_count} frames captured)")
    print("\nYour camera is working. You can now run:")
    print("python demo_identity_verification.py")
else:
    print(f"\n⚠️  Only captured {frame_count} frames")
    print("There may be a camera access issue.")




