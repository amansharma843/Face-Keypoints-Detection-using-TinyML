"""
Tests for Facial Landmark Detection Module
"""

import pytest
import numpy as np
import cv2
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from landmark_detector import FaceLandmarkDetector


class TestFaceLandmarkDetector:
    """Test suite for FaceLandmarkDetector."""
    
    @pytest.fixture
    def detector(self):
        """Create detector instance."""
        return FaceLandmarkDetector(static_image_mode=True)
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample image (synthetic face)."""
        # Create a 640x480 BGR image with a simple face-like pattern
        img = np.ones((480, 640, 3), dtype=np.uint8) * 200
        
        # Draw a simple face pattern
        center = (320, 240)
        # Face circle
        cv2.circle(img, center, 150, (180, 150, 120), -1)
        # Eyes
        cv2.circle(img, (270, 200), 20, (50, 50, 50), -1)
        cv2.circle(img, (370, 200), 20, (50, 50, 50), -1)
        # Nose
        cv2.ellipse(img, (320, 250), (15, 25), 0, 0, 360, (160, 130, 100), -1)
        # Mouth
        cv2.ellipse(img, (320, 310), (50, 25), 0, 0, 180, (100, 50, 50), -1)
        
        return img
    
    def test_detector_initialization(self, detector):
        """Test that detector initializes properly."""
        assert detector is not None
        assert detector.face_mesh is not None
    
    def test_detect_returns_none_on_no_face(self, detector):
        """Test that detect returns None when no face is present."""
        # Create blank image
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        landmarks = detector.detect(blank_image)
        assert landmarks is None
    
    def test_detect_returns_landmarks_shape(self, detector, sample_image):
        """Test that landmarks have correct shape if detected."""
        landmarks = detector.detect(sample_image)
        
        # May or may not detect face in synthetic image
        if landmarks is not None:
            assert landmarks.shape[1] == 3  # x, y, z coordinates
            assert landmarks.shape[0] == 478  # MediaPipe returns 478 landmarks
    
    def test_normalize_landmarks(self, detector):
        """Test landmark normalization."""
        # Create sample landmarks
        landmarks = np.random.randn(478, 3) * 100 + 300
        
        normalized = detector.normalize_landmarks(landmarks)
        
        # Check shape preserved
        assert normalized.shape == landmarks.shape
        
        # Check centered (mean should be close to 0)
        assert np.abs(normalized.mean()) < 1.0
    
    def test_get_key_landmarks(self, detector):
        """Test key landmark extraction."""
        # Create sample landmarks
        landmarks = np.random.randn(478, 3) * 100
        
        key_landmarks = detector.get_key_landmarks(landmarks)
        
        # Check all expected keys present
        expected_keys = [
            'left_eye_left', 'left_eye_right', 'right_eye_left', 'right_eye_right',
            'nose_tip', 'nose_bottom', 'mouth_left', 'mouth_right', 'mouth_center',
            'chin', 'left_eyebrow', 'right_eyebrow'
        ]
        
        for key in expected_keys:
            assert key in key_landmarks
            assert key_landmarks[key].shape == (3,)
    
    def test_draw_landmarks(self, detector, sample_image):
        """Test landmark drawing."""
        # Create sample landmarks
        h, w = sample_image.shape[:2]
        landmarks = np.random.rand(478, 3)
        landmarks[:, 0] *= w  # Scale x
        landmarks[:, 1] *= h  # Scale y
        landmarks[:, 2] *= 100  # Depth
        
        annotated = detector.draw_landmarks(sample_image, landmarks)
        
        # Check that image was modified
        assert annotated.shape == sample_image.shape
        assert not np.array_equal(annotated, sample_image)
    
    def test_detector_close(self, detector):
        """Test that detector can be closed without error."""
        try:
            detector.close()
        except Exception as e:
            pytest.fail(f"Detector close raised exception: {e}")


def test_sample_image_creation():
    """Test that sample image fixture works."""
    img = np.ones((480, 640, 3), dtype=np.uint8) * 200
    assert img.shape == (480, 640, 3)
    assert img.dtype == np.uint8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

