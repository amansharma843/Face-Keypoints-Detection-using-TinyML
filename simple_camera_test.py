#!/usr/bin/env python3
"""
Simple camera test with better error handling
"""

import cv2
import sys

print("=" * 60)
print("🎥 CAMERA TEST")
print("=" * 60)

# Try to open camera
print("\n1. Opening camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ FAILED: Camera won't open")
    print("\nFix:")
    print("  1. System Settings → Privacy & Security → Camera")
    print("  2. Enable 'Terminal' or 'Python'")
    print("  3. Restart Terminal and try again")
    sys.exit(1)

print("✅ Camera opened")

# Try to read a frame
print("\n2. Reading first frame...")
ret, frame = cap.read()

if not ret or frame is None:
    print("❌ FAILED: Can't read frames")
    print("\nThis means macOS is blocking camera access.")
    print("\nFix:")
    print("  1. Close this program")
    print("  2. System Settings → Privacy & Security → Camera")
    print("  3. Look for 'Terminal' or 'Python' and ENABLE it")
    print("  4. Quit Terminal completely (Cmd+Q)")
    print("  5. Reopen Terminal and try again")
    cap.release()
    sys.exit(1)

print(f"✅ Frame read successfully! Size: {frame.shape}")

# Show a few frames
print("\n3. Testing continuous frame reading...")
print("   Press 'q' in the window to quit\n")

frame_count = 0
while True:
    ret, frame = cap.read()
    
    if not ret:
        print(f"❌ Failed at frame {frame_count}")
        break
    
    frame_count += 1
    
    # Add text
    cv2.putText(frame, f"Frame {frame_count} - Press Q to quit", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Camera is working!", 
                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.imshow('Camera Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"\n✅ SUCCESS! Read {frame_count} frames")
        print("\n🎉 Your camera is working!")
        print("\nNow you can run:")
        print("  python demo_identity_verification.py")
        break
    
    if frame_count >= 100:
        print(f"\n✅ SUCCESS! Camera working perfectly ({frame_count} frames)")
        break

cap.release()
cv2.destroyAllWindows()

if frame_count < 10:
    print("\n⚠️  Only got a few frames. Check camera permissions.")
else:
    print("\n✅ Camera test PASSED!")




