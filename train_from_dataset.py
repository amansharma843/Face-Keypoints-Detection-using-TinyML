#!/usr/bin/env python3
"""
Train HDC Model from Dataset

Folder structure:
data/faces/
├── person1/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── img3.jpg
├── person2/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── img3.jpg
└── person3/
    ├── img1.jpg
    └── img2.jpg
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from identity_verifier import IdentityVerifier
import cv2
import glob

def train_from_folder(data_folder: str, model_save_path: str):
    """
    Train HDC model from folder of face images.
    
    Args:
        data_folder: Path to folder containing person folders
        model_save_path: Where to save trained model
    """
    print("=" * 70)
    print("🎓 TRAINING HDC MODEL FROM DATASET")
    print("=" * 70)
    
    # Initialize verifier
    verifier = IdentityVerifier(hv_dim=10000, levels=100)
    
    # Find all person folders
    person_folders = [f for f in os.listdir(data_folder) 
                     if os.path.isdir(os.path.join(data_folder, f))]
    
    if not person_folders:
        print(f"❌ No person folders found in {data_folder}")
        return
    
    print(f"\nFound {len(person_folders)} people to train on:")
    for person in person_folders:
        print(f"  - {person}")
    
    print("\n" + "=" * 70)
    print("ENROLLMENT PHASE")
    print("=" * 70)
    
    total_enrolled = 0
    total_samples = 0
    
    # Enroll each person
    for person_name in person_folders:
        person_path = os.path.join(data_folder, person_name)
        
        # Find all images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            image_files.extend(glob.glob(os.path.join(person_path, ext)))
        
        if not image_files:
            print(f"\n⚠️  No images found for {person_name}, skipping...")
            continue
        
        print(f"\n📝 Enrolling {person_name} ({len(image_files)} images)...")
        
        samples_enrolled = 0
        
        # Enroll each image
        for img_path in image_files:
            # Read image
            img = cv2.imread(img_path)
            if img is None:
                print(f"  ⚠️  Could not read {os.path.basename(img_path)}")
                continue
            
            # Enroll
            result = verifier.enroll_user(person_name, img, num_samples=len(image_files))
            
            if result['success']:
                samples_enrolled = result['num_samples']
                print(f"  ✅ Sample {samples_enrolled}/{len(image_files)}: {os.path.basename(img_path)}")
            else:
                print(f"  ❌ Failed: {result['message']}")
        
        if 'enrolled successfully' in verifier.get_enrolled_users():
            total_enrolled += 1
            total_samples += samples_enrolled
            print(f"  🎉 {person_name} enrolled with {samples_enrolled} samples!")
    
    # Training summary
    print("\n" + "=" * 70)
    print("📊 TRAINING SUMMARY")
    print("=" * 70)
    
    stats = verifier.get_stats()
    enrolled_users = verifier.get_enrolled_users()
    
    print(f"\n✅ Training complete!")
    print(f"  Total people enrolled: {len(enrolled_users)}")
    print(f"  Total samples processed: {total_samples}")
    print(f"  Memory usage: {stats['memory_usage']['total_kb']:.2f} KB")
    
    print(f"\nEnrolled users:")
    for i, user in enumerate(enrolled_users, 1):
        print(f"  {i}. {user}")
    
    # Save model
    print(f"\n💾 Saving model to {model_save_path}...")
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    verifier.save_model(model_save_path)
    
    print("\n" + "=" * 70)
    print("✅ MODEL TRAINING COMPLETE!")
    print("=" * 70)
    
    print(f"\n🎯 Your HDC model is ready!")
    print(f"  Model file: {model_save_path}")
    print(f"  Users: {len(enrolled_users)}")
    print(f"  Size: {stats['memory_usage']['total_kb']:.2f} KB")
    
    print(f"\n📝 To use this model:")
    print(f"  1. Load it: verifier.load_model('{model_save_path}')")
    print(f"  2. Or use in demo: Press 'l' and select this file")
    
    verifier.close()


def main():
    """Run training from command line."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train HDC model from dataset')
    parser.add_argument('--data', default='data/faces',
                       help='Path to dataset folder (default: data/faces)')
    parser.add_argument('--output', default='results/trained_model.pkl',
                       help='Where to save model (default: results/trained_model.pkl)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.data):
        print(f"❌ Dataset folder not found: {args.data}")
        print(f"\nCreate it with this structure:")
        print(f"  {args.data}/")
        print(f"  ├── person1/")
        print(f"  │   ├── img1.jpg")
        print(f"  │   └── img2.jpg")
        print(f"  └── person2/")
        print(f"      ├── img1.jpg")
        print(f"      └── img2.jpg")
        return
    
    train_from_folder(args.data, args.output)


if __name__ == "__main__":
    main()




