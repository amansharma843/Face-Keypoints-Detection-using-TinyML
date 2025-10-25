#!/usr/bin/env python3
"""
🔐 Interactive Identity Verification Demo
Test the complete HDC-based face verification system with your webcam

Controls:
    'e' - Enroll new user
    'v' - Verify identity
    'i' - Identify (who am I?)
    'u' - Update user profile (continual learning)
    's' - Save model
    'l' - Load model
    't' - Show statistics
    'q' - Quit
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from identity_verifier import IdentityVerifier
import cv2
import numpy as np


class InteractiveDemo:
    """Interactive demo for testing identity verification."""
    
    def __init__(self):
        """Initialize demo."""
        # Use 200 frames for maximum robust HDC training (best accuracy!)
        self.verifier = IdentityVerifier(hv_dim=15000, levels=150, enrollment_samples=200)
        self.current_user = None
        self.mode = "idle"
        self.enrollment_samples = []
        self.target_samples = 200  # Collect 200 frames for excellent accuracy (~94%)
        self.frame_skip = 0  # Collect every frame (no skipping)
        
    def draw_ui(self, frame: np.ndarray) -> np.ndarray:
        """Draw user interface on frame."""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Semi-transparent background for text
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Title
        cv2.putText(frame, "HDC IDENTITY VERIFICATION SYSTEM", 
                   (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2)
        
        # Mode indicator
        mode_colors = {
            'idle': (200, 200, 200),
            'enrolling': (0, 165, 255),  # Orange
            'verifying': (0, 255, 0),     # Green
            'identifying': (255, 0, 255), # Magenta
            'updating': (255, 255, 0)     # Cyan
        }
        
        mode_text = f"Mode: {self.mode.upper()}"
        if self.current_user:
            mode_text += f" | User: {self.current_user}"
        
        cv2.putText(frame, mode_text, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_colors.get(self.mode, (255, 255, 255)), 2)
        
        # Instructions
        instructions = "Press: [E]nroll | [V]erify | [I]dentify | [U]pdate | [S]ave | [T]stats | [Q]uit"
        cv2.putText(frame, instructions, (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Enrollment progress
        if self.mode == 'enrolling':
            progress = len(self.enrollment_samples)
            progress_text = f"Collecting: {progress}/{self.target_samples} frames"
            progress_pct = (progress / self.target_samples) * 100
            cv2.putText(frame, progress_text, (10, 115), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
            # Progress bar
            bar_width = 300
            bar_filled = int((progress / self.target_samples) * bar_width)
            cv2.rectangle(frame, (10, 125), (10 + bar_width, 140), (100, 100, 100), -1)
            cv2.rectangle(frame, (10, 125), (10 + bar_filled, 140), (0, 255, 0), -1)
        
        # Enrolled users list
        enrolled = self.verifier.get_enrolled_users()
        if enrolled:
            y_offset = 150
            cv2.putText(frame, f"Enrolled Users ({len(enrolled)}):", 
                       (w - 250, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            for i, user in enumerate(enrolled[:5]):  # Show max 5
                y_offset += 25
                cv2.putText(frame, f"  {i+1}. {user}", 
                           (w - 250, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            if len(enrolled) > 5:
                y_offset += 25
                cv2.putText(frame, f"  ... +{len(enrolled)-5} more", 
                           (w - 250, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
        
        return frame
    
    def show_result(self, frame: np.ndarray, result: dict, duration: int = 2000):
        """Show result overlay."""
        h, w = frame.shape[:2]
        overlay = frame.copy()
        
        # Result box
        box_h = 150
        box_w = 400
        box_x = (w - box_w) // 2
        box_y = (h - box_h) // 2
        
        # Background
        cv2.rectangle(overlay, (box_x, box_y), (box_x + box_w, box_y + box_h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Border color based on result
        if 'verified' in result:
            border_color = (0, 255, 0) if result['verified'] else (0, 0, 255)
        elif 'identified' in result:
            border_color = (255, 0, 255) if result['identified'] else (0, 0, 255)
        else:
            border_color = (255, 255, 255)
        
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_w, box_y + box_h), border_color, 3)
        
        # Result text
        y_offset = box_y + 40
        cv2.putText(frame, result.get('message', 'Result'), 
                   (box_x + 20, y_offset), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
        
        if 'confidence' in result:
            y_offset += 35
            confidence_pct = result['confidence'] * 100
            cv2.putText(frame, f"Confidence: {confidence_pct:.1f}%", 
                       (box_x + 20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        if 'inference_time_ms' in result:
            y_offset += 30
            cv2.putText(frame, f"Time: {result['inference_time_ms']:.1f} ms", 
                       (box_x + 20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        cv2.imshow('Identity Verification Demo', frame)
        cv2.waitKey(duration)
    
    def enroll_mode(self, frame: np.ndarray):
        """Handle enrollment - fast collection."""
        if self.current_user is None:
            return
        
        # Fast collection: enroll every frame
        result = self.verifier.enroll_user(self.current_user, frame, num_samples=self.target_samples)
        
        if result['success']:
            self.enrollment_samples.append(frame)
            
            # Show progress in terminal every 10 frames
            if len(self.enrollment_samples) % 10 == 0:
                pct = (len(self.enrollment_samples) / self.target_samples) * 100
                print(f"   Progress: {len(self.enrollment_samples)}/{self.target_samples} ({pct:.0f}%)")
            
            if 'enrolled successfully' in result['message']:
                self.show_result(frame, {
                    'message': f"✅ {self.current_user} enrolled with {len(self.enrollment_samples)} frames!",
                    'confidence': 1.0
                })
                self.mode = 'idle'
                self.enrollment_samples = []
                self.current_user = None
    
    def verify_mode(self, frame: np.ndarray):
        """Handle verification."""
        if self.current_user is None:
            return
        
        # Use stricter threshold for better discrimination
        result = self.verifier.verify(self.current_user, frame, threshold=0.80)
        
        # Add actual predicted ID to see who system thinks you are
        predicted_msg = f"System thinks you are: {result['predicted_id']}"
        if result['verified']:
            result['message'] = f"✅ Verified as {self.current_user}"
        else:
            result['message'] = f"❌ Not {self.current_user}. {predicted_msg}"
        
        # Show result
        self.show_result(frame, result)
        self.mode = 'idle'
        self.current_user = None
    
    def identify_mode(self, frame: np.ndarray):
        """Handle identification."""
        result = self.verifier.identify(frame, threshold=0.70)
        
        # Add more details to result
        if result['identified']:
            result['message'] = f"Identified as {result['user_id']}"
        else:
            result['message'] = "Unknown person"
        
        # Show result
        self.show_result(frame, result)
        self.mode = 'idle'
    
    def update_mode(self, frame: np.ndarray):
        """Handle user update (continual learning)."""
        if self.current_user is None:
            return
        
        result = self.verifier.update_user(self.current_user, frame, alpha=0.1)
        
        # Show result
        self.show_result(frame, result, duration=1500)
        self.mode = 'idle'
        self.current_user = None
    
    def get_user_input(self, prompt: str) -> str:
        """Get text input from user."""
        print(f"\n{prompt}")
        return input("> ").strip()
    
    def show_statistics(self):
        """Display system statistics."""
        print("\n" + "=" * 60)
        print("📊 SYSTEM STATISTICS")
        print("=" * 60)
        
        stats = self.verifier.get_stats()
        
        print("\nOperations:")
        print(f"  Enrollments: {stats['enrollments']}")
        print(f"  Verifications: {stats['verifications']}")
        print(f"  Updates: {stats['updates']}")
        print(f"  Detections: {stats['detections']}")
        print(f"  Detection failures: {stats['detection_failures']}")
        
        print(f"\nEnrolled Users: {stats['num_enrolled_users']}")
        for user in self.verifier.get_enrolled_users():
            print(f"  - {user}")
        
        print("\nMemory Usage:")
        mem = stats['memory_usage']
        for key, value in mem.items():
            if 'kb' in key:
                print(f"  {key}: {value:.2f} KB")
            else:
                print(f"  {key}: {value}")
        
        print(f"\n  Total: {mem['total_kb']:.2f} KB ({mem['total_kb']/1024:.2f} MB)")
        print("=" * 60)
    
    def run(self):
        """Run the interactive demo."""
        print("=" * 60)
        print("🔐 HDC IDENTITY VERIFICATION SYSTEM")
        print("=" * 60)
        print("\nInitializing webcam...")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Could not open webcam")
            return
        
        print("✅ Webcam ready!")
        print("\nControls:")
        print("  'e' - Enroll new user")
        print("  'v' - Verify identity")
        print("  'i' - Identify (who am I?)")
        print("  'u' - Update user profile")
        print("  's' - Save model")
        print("  'l' - Load model")
        print("  't' - Show statistics")
        print("  'q' - Quit")
        print("\nPress any key to start...")
        
        cv2.namedWindow('Identity Verification Demo')
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error reading frame")
                break
            
            # Detect landmarks and draw them on frame
            landmarks = self.verifier.detector.detect(frame)
            
            if landmarks is not None:
                # Draw all 478 keypoints (green dots)
                display_frame = self.verifier.detector.draw_landmarks(frame, landmarks)
            else:
                display_frame = frame.copy()
            
            # Process based on mode
            if self.mode == 'enrolling':
                self.enroll_mode(display_frame)
            elif self.mode == 'verifying':
                self.verify_mode(display_frame)
            elif self.mode == 'identifying':
                self.identify_mode(display_frame)
            elif self.mode == 'updating':
                self.update_mode(display_frame)
            
            # Draw UI on top of landmarks
            display_frame = self.draw_ui(display_frame)
            
            # Show frame
            cv2.imshow('Identity Verification Demo', display_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n👋 Quitting...")
                break
            
            elif key == ord('e'):
                # Start enrollment
                user_id = self.get_user_input("Enter user ID to enroll:")
                if user_id:
                    self.current_user = user_id
                    self.mode = 'enrolling'
                    self.enrollment_samples = []
                    print(f"📝 Enrolling {user_id}...")
                    print(f"   Collecting {self.target_samples} frames automatically...")
                    print(f"   Stay still and look at the camera!")
            
            elif key == ord('v'):
                # Start verification
                user_id = self.get_user_input("Enter user ID to verify:")
                if user_id:
                    self.current_user = user_id
                    self.mode = 'verifying'
                    print(f"🔍 Verifying {user_id}. Look at camera and press any key...")
                    print(f"   Note: Need confidence > 0.75 to verify")
            
            elif key == ord('i'):
                # Identify
                self.mode = 'identifying'
                self.identify_mode(frame)
            
            elif key == ord('u'):
                # Update user
                user_id = self.get_user_input("Enter user ID to update:")
                if user_id:
                    self.current_user = user_id
                    self.mode = 'updating'
                    print(f"🔄 Updating {user_id}. Look at camera and press any key...")
            
            elif key == ord('s'):
                # Save model
                filepath = "results/identity_model.pkl"
                self.verifier.save_model(filepath)
                print(f"💾 Model saved to {filepath}")
            
            elif key == ord('l'):
                # Load model
                filepath = "results/identity_model.pkl"
                if os.path.exists(filepath):
                    self.verifier.load_model(filepath)
                    print(f"📂 Model loaded from {filepath}")
                else:
                    print(f"❌ Model file not found: {filepath}")
            
            elif key == ord('t'):
                # Show statistics
                self.show_statistics()
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.verifier.close()
        print("\n✅ Demo complete!")


def main():
    """Run the demo."""
    demo = InteractiveDemo()
    demo.run()


if __name__ == "__main__":
    main()

