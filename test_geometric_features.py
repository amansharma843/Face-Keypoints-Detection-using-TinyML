"""
Tests for Geometric Feature Extraction Module
"""

import pytest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from geometric_features import GeometricFeatureExtractor


class TestGeometricFeatureExtractor:
    """Test suite for GeometricFeatureExtractor."""
    
    @pytest.fixture
    def extractor(self):
        """Create feature extractor instance."""
        return GeometricFeatureExtractor()
    
    @pytest.fixture
    def sample_landmarks(self):
        """Create sample landmarks."""
        np.random.seed(42)
        landmarks = np.random.randn(478, 3) * 100 + 300
        return landmarks
    
    def test_extractor_initialization(self, extractor):
        """Test that extractor initializes properly."""
        assert extractor is not None
        assert len(extractor.key_pairs) > 0
        assert len(extractor.key_triplets) > 0
    
    def test_extract_distance_features(self, extractor, sample_landmarks):
        """Test distance feature extraction."""
        features = extractor.extract_distance_features(sample_landmarks)
        
        # Check correct number of features
        assert len(features) == len(extractor.key_pairs)
        
        # Check all features are non-negative
        assert np.all(features >= 0)
        
        # Check no NaN or inf values
        assert not np.any(np.isnan(features))
        assert not np.any(np.isinf(features))
    
    def test_extract_ratio_features(self, extractor, sample_landmarks):
        """Test ratio feature extraction."""
        features = extractor.extract_ratio_features(sample_landmarks)
        
        # Check correct number of features
        assert len(features) == len(extractor.key_pairs)
        
        # Check all features are non-negative
        assert np.all(features >= 0)
        
        # Check no NaN or inf values
        assert not np.any(np.isnan(features))
        assert not np.any(np.isinf(features))
    
    def test_extract_angle_features(self, extractor, sample_landmarks):
        """Test angle feature extraction."""
        features = extractor.extract_angle_features(sample_landmarks)
        
        # Check correct number of features
        assert len(features) == len(extractor.key_triplets)
        
        # Check angles are in valid range [0, π]
        assert np.all(features >= 0)
        assert np.all(features <= np.pi)
        
        # Check no NaN or inf values
        assert not np.any(np.isnan(features))
        assert not np.any(np.isinf(features))
    
    def test_extract_all_features(self, extractor, sample_landmarks):
        """Test extraction of all feature types."""
        features = extractor.extract_all_features(sample_landmarks)
        
        # Check dictionary has all keys
        assert 'distances' in features
        assert 'ratios' in features
        assert 'angles' in features
        
        # Check each feature type
        assert len(features['distances']) == len(extractor.key_pairs)
        assert len(features['ratios']) == len(extractor.key_pairs)
        assert len(features['angles']) == len(extractor.key_triplets)
    
    def test_get_feature_vector(self, extractor, sample_landmarks):
        """Test concatenated feature vector."""
        feature_vector = extractor.get_feature_vector(sample_landmarks)
        
        # Calculate expected length
        expected_len = 2 * len(extractor.key_pairs) + len(extractor.key_triplets)
        assert len(feature_vector) == expected_len
        
        # Check no NaN or inf values
        assert not np.any(np.isnan(feature_vector))
        assert not np.any(np.isinf(feature_vector))
    
    def test_get_feature_names(self, extractor):
        """Test feature name generation."""
        names = extractor.get_feature_names()
        
        # Calculate expected number of names
        expected_count = 2 * len(extractor.key_pairs) + len(extractor.key_triplets)
        assert len(names) == expected_count
        
        # Check all names are strings
        assert all(isinstance(name, str) for name in names)
        
        # Check name prefixes
        distance_names = [n for n in names if n.startswith('dist_')]
        ratio_names = [n for n in names if n.startswith('ratio_')]
        angle_names = [n for n in names if n.startswith('angle_')]
        
        assert len(distance_names) == len(extractor.key_pairs)
        assert len(ratio_names) == len(extractor.key_pairs)
        assert len(angle_names) == len(extractor.key_triplets)
    
    def test_feature_consistency(self, extractor, sample_landmarks):
        """Test that same landmarks produce same features."""
        features1 = extractor.get_feature_vector(sample_landmarks)
        features2 = extractor.get_feature_vector(sample_landmarks)
        
        np.testing.assert_array_almost_equal(features1, features2)
    
    def test_scale_invariance_of_ratios(self, extractor, sample_landmarks):
        """Test that ratio features are scale-invariant."""
        # Get features from original landmarks
        features1 = extractor.extract_ratio_features(sample_landmarks)
        
        # Scale landmarks by 2
        scaled_landmarks = sample_landmarks * 2.0
        features2 = extractor.extract_ratio_features(scaled_landmarks)
        
        # Ratio features should be identical
        np.testing.assert_array_almost_equal(features1, features2, decimal=5)
    
    def test_zero_distance_handling(self, extractor):
        """Test handling of zero distances."""
        # Create landmarks where some points are identical
        landmarks = np.zeros((478, 3))
        
        # This should not crash
        try:
            features = extractor.get_feature_vector(landmarks)
            # Check that features are valid (0 or inf handled properly)
            assert len(features) > 0
        except Exception as e:
            pytest.fail(f"Zero distance handling failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

