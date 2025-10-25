#!/bin/bash

echo "🚀 Setting up Facial Keypoint TinyML Thesis Project"
echo "=================================================="
echo ""

# Step 1: Create virtual environment
echo "📦 Step 1/5: Creating virtual environment..."
python3 -m venv venv
if [ $? -eq 0 ]; then
    echo "✅ Virtual environment created successfully"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi
echo ""

# Step 2: Activate virtual environment
echo "🔌 Step 2/5: Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Step 3: Upgrade pip
echo "⬆️  Step 3/5: Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "✅ Pip upgraded"
echo ""

# Step 4: Install all packages
echo "📚 Step 4/5: Installing packages (this may take 5-10 minutes)..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully"
else
    echo "❌ Some packages failed to install. Check errors above."
    exit 1
fi
echo ""

# Step 5: Verify installation
echo "🔍 Step 5/5: Verifying installation..."
python3 verify_installation.py
echo ""

echo "🎉 Setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""

