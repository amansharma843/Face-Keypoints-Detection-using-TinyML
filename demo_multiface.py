#!/usr/bin/env python3
"""
🎭 MULTI-FACE RECOGNITION DEMO
Beautiful UI with real-time multiple face detection and identification

Features:
- Detect up to 5 faces simultaneously
- Identify each person with name labels
- Beautiful bounding boxes and confidence scores
- Modern UI design
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from identity_verifier import IdentityVerifier
import cv2
import numpy as np

# Color palette (modern, beautiful colors)
COLORS = {
    'primary': (0, 200, 255),      # Cyan
    'success': (0, 255, 100),      # Green
    'warning': (0, 165, 255),      # Orange
    'danger': (0, 0, 255),         # Red
    'info': (255, 200, 0),         # Blue
    'text': (255, 255, 255),       # White
    'bg_dark': (20, 20, 20),       # Dark gray
    'bg_light': (240, 240, 240),   # Light gray
}

def draw_modern_box(image, x1, y1, x2, y2, color, thickness=2):
    """Draw modern rounded corner box."""
    corner_length = 20
    
    # Top-left corner
    cv2.line(image, (x1, y1 + corner_length), (x1, y1), color, thickness)
    cv2.line(image, (x1, y1), (x1 + corner_length, y1), color, thickness)
    
    # Top-right corner
    cv2.line(image, (x2 - corner_length, y1), (x2, y1), color, thickness)
    cv2.line(image, (x2, y1), (x2, y1 + corner_length), color, thickness)
    
    # Bottom-left corner
    cv2.line(image, (x1, y2 - corner_length), (x1, y2), color, thickness)
    cv2.line(image, (x1, y2), (x1 + corner_length, y2), color, thickness)
    
    # Bottom-right corner
    cv2.line(image, (x2 - corner_length, y2), (x2, y2), color, thickness)
    cv2.line(image, (x2, y2), (x2, y2 - corner_length), color, thickness)

def draw_label_box(image, text, x, y, color, confidence=None):
    """Draw beautiful label box with text."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Add confidence if provided
    if confidence is not None:
        conf_text = f" {confidence*100:.0f}%"
        (conf_width, _), _ = cv2.getTextSize(conf_text, font, font_scale * 0.8, thickness)
        text_width += conf_width
    
    # Draw background box (with alpha)
    padding = 10
    box_x1 = x - padding
    box_y1 = y - text_height - padding * 2
    box_x2 = x + text_width + padding
    box_y2 = y + padding
    
    # Create overlay for transparency
    overlay = image.copy()
    cv2.rectangle(overlay, (box_x1, box_y1), (box_x2, box_y2), color, -1)
    cv2.addWeighted(overlay, 0.8, image, 0.2, 0, image)
    
    # Draw border
    cv2.rectangle(image, (box_x1, box_y1), (box_x2, box_y2), color, 2)
    
    # Draw text
    cv2.putText(image, text, (x, y - padding), font, font_scale, COLORS['text'], thickness)
    
    # Draw confidence
    if confidence is not None:
        cv2.putText(image, conf_text, (x + text_width - conf_width, y - padding), 
                   font, font_scale * 0.8, COLORS['bg_light'], thickness)

def get_face_bbox(landmarks):
    """Get bounding box from landmarks."""
    x_coords = landmarks[:, 0]
    y_coords = landmarks[:, 1]
    
    x_min, x_max = int(x_coords.min()), int(x_coords.max())
    y_min, y_max = int(y_coords.min()), int(y_coords.max())
    
    # Add padding
    padding = 20
    x_min = max(0, x_min - padding)
    y_min = max(0, y_min - padding)
    x_max += padding
    y_max += padding
    
    return x_min, y_min, x_max, y_max

def draw_header(image, num_faces, num_enrolled):
    """Draw beautiful header."""
    h, w = image.shape[:2]
    
    # Semi-transparent header bar
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), COLORS['bg_dark'], -1)
    cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
    
    # Title
    cv2.putText(image, "HDC MULTI-FACE RECOGNITION", (20, 35), 
               cv2.FONT_HERSHEY_DUPLEX, 0.9, COLORS['primary'], 2)
    
    # Stats
    stats_text = f"Faces: {num_faces} | Database: {num_enrolled} users"
    cv2.putText(image, stats_text, (20, 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['text'], 1)
    
    # FPS (placeholder)
    cv2.putText(image, "Live", (w - 80, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['success'], 2)

def draw_footer(image, message="Press 'q' to quit | 'e' to enroll | 'i' for info"):
    """Draw beautiful footer."""
    h, w = image.shape[:2]
    
    # Semi-transparent footer bar
    overlay = image.copy()
    cv2.rectangle(overlay, (0, h - 40), (w, h), COLORS['bg_dark'], -1)
    cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
    
    # Message
    cv2.putText(image, message, (20, h - 15), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['text'], 1)

def main():
    """Run multi-face recognition demo."""
    print("=" * 70)
    print("🎭 MULTI-FACE RECOGNITION SYSTEM")
    print("=" * 70)
    print("\nFeatures:")
    print("  • Detect up to 5 faces simultaneously")
    print("  • Identify each person in real-time")
    print("  • Beautiful modern UI")
    print("\nControls:")
    print("  'q' - Quit")
    print("  'i' - Show info")
    print("=" * 70)
    
    # Initialize system with optimized parameters
    print("\nInitializing with optimized HDC parameters...")
    verifier = IdentityVerifier(hv_dim=15000, levels=150, enrollment_samples=200)
    
    # Load saved model if available
    if os.path.exists("results/identity_model.pkl"):
        verifier.load_model("results/identity_model.pkl")
        print(f"✅ Loaded model with {len(verifier.get_enrolled_users())} users")
    else:
        print("⚠️  No saved model found. Please enroll users first.")
        print("   Run: python demo_identity_verification.py")
    
    # Open camera
    cap = cv2.VideoCapture(1)  # Try external camera first
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)  # Fallback to built-in
    
    if not cap.isOpened():
        print("❌ Cannot open camera")
        return
    
    print("✅ Camera ready!")
    print("\nStarting multi-face recognition...\n")
    
    cv2.namedWindow('Multi-Face Recognition', cv2.WINDOW_NORMAL)
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        h, w = frame.shape[:2]
        
        # Create display frame
        display = frame.copy()
        
        # Identify all faces at once with stricter threshold
        face_results = verifier.identify_all_faces(frame, threshold=0.70)
        num_faces = len(face_results)
        num_enrolled = len(verifier.get_enrolled_users())
        
        # Process each detected face
        recognized_count = 0
        unknown_count = 0
        
        for result in face_results:
            landmarks = result['landmarks']
            
            # Get bounding box
            x1, y1, x2, y2 = get_face_bbox(landmarks)
            
            # Determine display info
            if result['identified']:
                # Recognized person
                name = result['user_id']
                confidence = result['confidence']
                color = COLORS['success']
                recognized_count += 1
            elif num_enrolled > 0:
                # Unknown person
                name = "Unknown"
                confidence = result['confidence']
                color = COLORS['warning']
                unknown_count += 1
            else:
                # No database
                name = f"Face {result['face_index'] + 1}"
                confidence = None
                color = COLORS['info']
            
            # Draw modern bounding box
            draw_modern_box(display, x1, y1, x2, y2, color, thickness=3)
            
            # Draw name label
            draw_label_box(display, name, x1 + 5, y1 - 5, color, confidence)
            
            # Draw keypoints (every 5th point for better visibility)
            for i in range(0, len(landmarks), 5):
                x, y = int(landmarks[i][0]), int(landmarks[i][1])
                cv2.circle(display, (x, y), 2, color, -1)
        
        # Draw header
        draw_header(display, num_faces, num_enrolled)
        
        # Draw footer with dynamic message
        if num_faces == 0:
            footer_msg = "No faces detected - Looking for faces..."
        elif num_enrolled == 0:
            footer_msg = "No users in database - Enroll users first!"
        else:
            footer_msg = f"Recognized: {recognized_count} | Unknown: {unknown_count} | Press 'q' to quit"
        
        draw_footer(display, footer_msg)
        
        # Show frame
        cv2.imshow('Multi-Face Recognition', display)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Quitting...")
            break
        elif key == ord('i'):
            print(f"\n📊 System Info:")
            print(f"  Enrolled users: {num_enrolled}")
            print(f"  Current faces: {num_faces}")
            print(f"  Frame: {frame_count}")
            stats = verifier.get_stats()
            print(f"  Memory: {stats['memory_usage']['total_kb']:.1f} KB")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    verifier.close()
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    main()

