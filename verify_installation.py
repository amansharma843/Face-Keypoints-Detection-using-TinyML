#!/usr/bin/env python3
"""
Verification script to check if all required packages are installed correctly.
"""

import sys

def check_package(package_name, import_name=None):
    """Check if a package can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name:20s} - version {version}")
        return True
    except ImportError as e:
        print(f"❌ {package_name:20s} - NOT INSTALLED")
        return False

def main():
    print("=" * 60)
    print("INSTALLATION VERIFICATION")
    print("=" * 60)
    print()
    
    packages = [
        ('NumPy', 'numpy'),
        ('Pandas', 'pandas'),
        ('Matplotlib', 'matplotlib'),
        ('OpenCV', 'cv2'),
        ('PyTorch', 'torch'),
        ('TorchVision', 'torchvision'),
        ('TensorFlow', 'tensorflow'),
        ('MediaPipe', 'mediapipe'),
        ('Scikit-learn', 'sklearn'),
        ('Jupyter', 'jupyter'),
        ('TQDM', 'tqdm'),
        ('PyYAML', 'yaml'),
        ('Pillow', 'PIL'),
    ]
    
    results = []
    for package_name, import_name in packages:
        results.append(check_package(package_name, import_name))
    
    print()
    print("=" * 60)
    
    if all(results):
        print("🎉 ALL PACKAGES INSTALLED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("  1. Run: jupyter notebook")
        print("  2. Check out the example notebooks")
        print("  3. Start experimenting!")
    else:
        print("⚠️  SOME PACKAGES FAILED TO INSTALL")
        print()
        print("Please check the errors above and try:")
        print("  pip install -r requirements.txt")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())

