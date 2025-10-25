#!/usr/bin/env python3
"""
Export Trained HDC Model for Embedded Deployment (MAX78000)

This script converts your Python HDC model to formats suitable for:
1. C code generation
2. Binary model file for MAX78000
3. Performance analysis
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from identity_verifier import IdentityVerifier
import numpy as np
import pickle

def analyze_model_size(verifier):
    """Analyze model memory requirements."""
    print("\n" + "=" * 70)
    print("📊 MODEL SIZE ANALYSIS")
    print("=" * 70)
    
    stats = verifier.get_stats()
    mem = stats['memory_usage']
    
    # Calculate packed sizes for embedded
    hv_dim = verifier.encoder.hv_dim
    hv_bytes_packed = hv_dim // 8  # 10,000 bits = 1,250 bytes
    
    num_users = len(verifier.get_enrolled_users())
    
    print(f"\nPython (Current):")
    print(f"  Total memory: {mem['total_kb']:.2f} KB")
    print(f"  Basis HVs: {mem['basis_hvs_kb']:.2f} KB")
    print(f"  Level HVs: {mem['level_hvs_kb']:.2f} KB")
    print(f"  Prototypes: {mem['prototypes_kb']:.2f} KB")
    
    # Calculate embedded size (packed bits)
    basis_packed = (27 * hv_bytes_packed) / 1024  # KB
    level_packed = (100 * hv_bytes_packed) / 1024  # KB
    proto_packed = (num_users * hv_bytes_packed) / 1024  # KB
    total_packed = basis_packed + level_packed + proto_packed
    
    print(f"\nEmbedded (Optimized - Packed Bits):")
    print(f"  Total memory: {total_packed:.2f} KB")
    print(f"  Basis HVs: {basis_packed:.2f} KB")
    print(f"  Level HVs: {level_packed:.2f} KB")
    print(f"  Prototypes: {proto_packed:.2f} KB ({num_users} users)")
    
    print(f"\nCompression:")
    print(f"  Compression ratio: {mem['total_kb']/total_packed:.1f}×")
    print(f"  Savings: {mem['total_kb'] - total_packed:.2f} KB")
    
    print(f"\nMAX78000 Fit Check:")
    flash_size = 512  # KB
    sram_size = 128   # KB
    
    print(f"  Flash (model storage): {total_packed:.1f} KB / {flash_size} KB")
    print(f"    {'✅ FITS!' if total_packed < flash_size else '❌ TOO BIG'}")
    
    runtime_mem = total_packed + 20  # Add runtime overhead
    print(f"  SRAM (runtime): ~{runtime_mem:.1f} KB / {sram_size} KB")
    print(f"    {'✅ FITS!' if runtime_mem < sram_size else '❌ TOO BIG'}")
    
    return {
        'total_kb': total_packed,
        'fits_in_max78000': total_packed < flash_size and runtime_mem < sram_size
    }


def export_binary_model(verifier, output_path):
    """Export model as binary file for MAX78000."""
    print("\n" + "=" * 70)
    print("💾 EXPORTING BINARY MODEL")
    print("=" * 70)
    
    users = verifier.get_enrolled_users()
    
    if len(users) == 0:
        print("❌ No users enrolled! Train the model first.")
        return
    
    print(f"\nExporting {len(users)} users to binary format...")
    
    with open(output_path, 'wb') as f:
        # Header
        f.write(b'HDC1')  # Magic number
        f.write(len(users).to_bytes(4, 'little'))
        f.write(verifier.encoder.hv_dim.to_bytes(4, 'little'))
        f.write(verifier.encoder.input_dim.to_bytes(4, 'little'))
        f.write(verifier.encoder.levels.to_bytes(4, 'little'))
        
        # User prototypes
        for user in users:
            # User name (32 bytes, null-padded)
            name_bytes = user.encode('utf-8')[:32]
            name_bytes = name_bytes.ljust(32, b'\x00')
            f.write(name_bytes)
            
            # Prototype (packed bits)
            prototype = verifier.encoder.class_prototypes[user]
            packed = np.packbits(prototype.astype(np.uint8))
            f.write(packed.tobytes())
        
        # Basis hypervectors
        for i in range(verifier.encoder.input_dim):
            packed = np.packbits(verifier.encoder.basis_hvs[i].astype(np.uint8))
            f.write(packed.tobytes())
        
        # Level hypervectors
        for i in range(verifier.encoder.levels):
            packed = np.packbits(verifier.encoder.level_hvs[i].astype(np.uint8))
            f.write(packed.tobytes())
    
    file_size = os.path.getsize(output_path)
    print(f"\n✅ Binary model exported!")
    print(f"  File: {output_path}")
    print(f"  Size: {file_size / 1024:.2f} KB")
    print(f"  Users: {len(users)}")


def generate_c_header(verifier, output_path):
    """Generate C header file with model constants."""
    print("\n" + "=" * 70)
    print("📝 GENERATING C HEADER FILE")
    print("=" * 70)
    
    with open(output_path, 'w') as f:
        f.write("// Auto-generated HDC model header\n")
        f.write("// Generated from Python HDC model\n\n")
        f.write("#ifndef HDC_MODEL_H\n")
        f.write("#define HDC_MODEL_H\n\n")
        f.write("#include <stdint.h>\n\n")
        
        # Constants
        f.write(f"#define HV_DIM {verifier.encoder.hv_dim}\n")
        f.write(f"#define HV_DIM_BYTES {verifier.encoder.hv_dim // 8}\n")
        f.write(f"#define HV_DIM_WORDS {verifier.encoder.hv_dim // 32}\n")
        f.write(f"#define NUM_FEATURES {verifier.encoder.input_dim}\n")
        f.write(f"#define NUM_LEVELS {verifier.encoder.levels}\n")
        f.write(f"#define NUM_USERS {len(verifier.get_enrolled_users())}\n\n")
        
        # Structures
        f.write("// User structure\n")
        f.write("typedef struct {\n")
        f.write("    char name[32];\n")
        f.write("    uint32_t prototype[HV_DIM_WORDS];\n")
        f.write("} User_t;\n\n")
        
        f.write("// Model structure\n")
        f.write("typedef struct {\n")
        f.write("    User_t users[NUM_USERS];\n")
        f.write("    uint32_t basis_hvs[NUM_FEATURES][HV_DIM_WORDS];\n")
        f.write("    uint32_t level_hvs[NUM_LEVELS][HV_DIM_WORDS];\n")
        f.write("    uint8_t num_users;\n")
        f.write("} HDC_Model_t;\n\n")
        
        f.write("#endif // HDC_MODEL_H\n")
    
    print(f"✅ C header generated: {output_path}")


def estimate_performance():
    """Estimate performance on MAX78000."""
    print("\n" + "=" * 70)
    print("⚡ ESTIMATED PERFORMANCE ON MAX78000")
    print("=" * 70)
    
    # Operation counts
    hv_dim = 10000
    num_features = 27
    
    # XOR operations per encoding
    xor_ops = num_features  # One XOR per feature
    
    # Bit counting for Hamming distance
    popcount_ops = hv_dim // 32  # Process 32 bits at a time
    
    # ARM Cortex-M4 @ 100 MHz estimates
    cycles_per_xor = 1  # Single cycle XOR on 32-bit
    cycles_per_popcount = 10  # With SIMD instruction
    
    # Encoding time
    xor_cycles = xor_ops * (hv_dim // 32) * cycles_per_xor
    encoding_time_ms = (xor_cycles / 100_000_000) * 1000
    
    # Verification time (Hamming distance)
    verify_cycles = popcount_ops * cycles_per_popcount
    verify_time_ms = (verify_cycles / 100_000_000) * 1000
    
    total_time_ms = encoding_time_ms + verify_time_ms
    
    print(f"\nOperation Analysis:")
    print(f"  Encoding operations: {xor_ops} XORs")
    print(f"  Hamming distance: {popcount_ops} popcounts")
    print(f"\nEstimated Timing (@ 100 MHz):")
    print(f"  Encoding: ~{encoding_time_ms:.2f} ms")
    print(f"  Verification: ~{verify_time_ms:.2f} ms")
    print(f"  Total: ~{total_time_ms:.2f} ms")
    
    # Power estimates
    active_power_mw = 5  # MAX78000 active power
    idle_power_mw = 0.2
    
    energy_uj = active_power_mw * total_time_ms
    
    print(f"\nPower Consumption:")
    print(f"  Active power: {active_power_mw} mW")
    print(f"  Energy per verification: ~{energy_uj:.1f} μJ")
    
    # Battery life
    battery_mah = 3000
    battery_v = 3.7
    battery_uwh = battery_mah * battery_v * 1000  # μWh
    
    verifications = battery_uwh / energy_uj
    
    print(f"\nBattery Life (3000 mAh):")
    print(f"  Max verifications: {verifications:,.0f}")
    print(f"  At 1/sec: {verifications / 3600:.1f} hours")
    print(f"  At 10/sec: {verifications / 36000:.1f} hours")
    
    # Comparison
    print(f"\nEfficiency Comparison:")
    cloud_energy = 750_000  # μJ (from earlier analysis)
    improvement = cloud_energy / energy_uj
    print(f"  vs Cloud GPU: {improvement:,.0f}× more efficient! ⚡")
    
    return {
        'inference_time_ms': total_time_ms,
        'energy_uj': energy_uj,
        'efficiency_vs_cloud': improvement
    }


def main():
    """Run export process."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export model for embedded deployment')
    parser.add_argument('--model', default='results/identity_model.pkl',
                       help='Path to trained model (default: results/identity_model.pkl)')
    parser.add_argument('--output-dir', default='max78000/',
                       help='Output directory (default: max78000/)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🔧 HDC MODEL EXPORT FOR EMBEDDED DEPLOYMENT")
    print("=" * 70)
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"\n❌ Model not found: {args.model}")
        print("\nPlease train a model first:")
        print("  1. Run: python demo_identity_verification.py")
        print("  2. Enroll users (press 'e')")
        print("  3. Save model (press 's')")
        return
    
    # Load model
    print(f"\n📂 Loading model: {args.model}")
    verifier = IdentityVerifier()
    verifier.load_model(args.model)
    
    users = verifier.get_enrolled_users()
    if not users:
        print("❌ No users in model! Train first.")
        return
    
    print(f"✅ Model loaded with {len(users)} users: {users}")
    
    # Analyze size
    size_info = analyze_model_size(verifier)
    
    if not size_info['fits_in_max78000']:
        print("\n⚠️  WARNING: Model may not fit in MAX78000!")
        print("    Consider reducing number of users or HV dimension.")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Export files
    binary_path = os.path.join(args.output_dir, 'model.bin')
    header_path = os.path.join(args.output_dir, 'hdc_model.h')
    
    export_binary_model(verifier, binary_path)
    generate_c_header(verifier, header_path)
    
    # Performance estimates
    perf = estimate_performance()
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ EXPORT COMPLETE!")
    print("=" * 70)
    
    print(f"\n📁 Generated Files:")
    print(f"  Binary model: {binary_path}")
    print(f"  C header: {header_path}")
    print(f"  Size: {size_info['total_kb']:.1f} KB")
    
    print(f"\n🎯 Deployment Ready:")
    print(f"  Target: MAX78000 microcontroller")
    print(f"  Inference: ~{perf['inference_time_ms']:.1f} ms")
    print(f"  Energy: ~{perf['energy_uj']:.0f} μJ")
    print(f"  Efficiency: {perf['efficiency_vs_cloud']:.0f}× better than cloud!")
    
    print(f"\n📖 Next Steps:")
    print(f"  1. Read: docs/EMBEDDED_DEPLOYMENT.md")
    print(f"  2. Implement C code using generated header")
    print(f"  3. Flash to MAX78000 board")
    print(f"  4. Test and measure real performance!")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()




