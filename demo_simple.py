#!/usr/bin/env python3
"""
Simple Face Verification Demo
Shows camera feed with face detection status
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from identity_verifier import IdentityVerifier
import cv2

print("=" * 60)
print("🔐 SIMPLE FACE VERIFICATION DEMO")
print("=" * 60)
print("\nThis demo will:")
print("1. Show your camera feed with face detection")
print("2. Auto-enroll you when face is detected")
print("3. Verify your identity")
print("\nControls:")
print("  Press 'q' to quit anytime")
print("=" * 60)

# Initialize
verifier = IdentityVerifier(hv_dim=10000, levels=100)

# Try camera 1 first (might be iPhone), then camera 0 (built-in Mac)
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Camera 1 not available, trying camera 0...")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit(1)

print("\n✅ Camera ready!")
print("\nStep 1: ENROLLMENT")
print("Position your face in the camera...")
print("Press SPACE when ready to enroll\n")

user_id = "Aman"
enrolled = False
verified = False
enrollment_samples = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Can't read frame")
        break
    
    # ALWAYS show the camera feed (even if black)
    display = frame.copy()
    
    # Try to detect face and extract features
    features = verifier.extract_features_from_image(frame)
    h, w = display.shape[:2]
    
    if features is not None:
        # Face detected!
        cv2.putText(display, "FACE DETECTED!", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if not enrolled:
            cv2.putText(display, f"Samples: {len(enrollment_samples)}/5", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(display, "Press SPACE to collect sample", (10, 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        elif not verified:
            cv2.putText(display, "ENROLLED! Press SPACE to verify", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(display, "VERIFIED! Press Q to quit", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        # No face detected
        cv2.putText(display, "NO FACE DETECTED", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(display, "Please face the camera", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
    
    cv2.putText(display, "Press Q to quit", (10, h - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    cv2.imshow('Face Verification Demo', display)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        print("\n👋 Quitting...")
        break
    
    elif key == 32 and features is not None:  # SPACE
        if not enrolled:
            # Collect enrollment sample
            result = verifier.enroll_user(user_id, frame, num_samples=5)
            enrollment_samples.append(frame)
            print(f"✅ Sample {len(enrollment_samples)}/5 collected")
            
            if 'enrolled successfully' in result['message']:
                enrolled = True
                print(f"\n🎉 {user_id} enrolled successfully!")
                print(f"\nStep 2: VERIFICATION")
                print("Press SPACE to verify your identity\n")
        
        elif not verified:
            # Verify
            print("🔍 Verifying...")
            result = verifier.verify(user_id, frame, threshold=0.7)
            
            print(f"\n{'='*60}")
            print(f"VERIFICATION RESULT:")
            print(f"{'='*60}")
            print(f"  Verified: {'✅ YES' if result['verified'] else '❌ NO'}")
            print(f"  Claimed ID: {result['claimed_id']}")
            print(f"  Predicted ID: {result['predicted_id']}")
            print(f"  Confidence: {result['confidence']:.4f} ({result['confidence']*100:.1f}%)")
            print(f"  Threshold: {result['threshold']}")
            print(f"  Inference Time: {result['inference_time_ms']:.2f} ms")
            print(f"{'='*60}\n")
            
            verified = True
            
            # Show stats
            stats = verifier.get_stats()
            print(f"System Stats:")
            print(f"  Memory: {stats['memory_usage']['total_kb']:.2f} KB")
            print(f"  Enrolled users: {stats['num_enrolled_users']}")
            print(f"\nPress Q to quit or SPACE to verify again")

cap.release()
cv2.destroyAllWindows()
verifier.close()

print("\n✅ Demo complete!")

