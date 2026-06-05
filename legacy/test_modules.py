"""
Module Test Script
Verify all components are working correctly
"""

import sys


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing module imports...")
    print("-" * 50)
    
    modules = {
        'PyQt6': 'PyQt6.QtWidgets',
        'qfluentwidgets': 'qfluentwidgets',
        'OpenCV': 'cv2',
        'NumPy': 'numpy',
        'Ultralytics': 'ultralytics',
        'Pillow': 'PIL'
    }
    
    failed = []
    
    for name, module in modules.items():
        try:
            __import__(module)
            print(f"✓ {name:20} OK")
        except ImportError as e:
            print(f"✗ {name:20} FAILED - {e}")
            failed.append(name)
    
    print("-" * 50)
    
    if failed:
        print(f"\n❌ {len(failed)} module(s) failed to import:")
        for name in failed:
            print(f"   - {name}")
        print("\nPlease install missing modules:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True


def test_project_files():
    """Test if all project files exist"""
    import os
    
    print("\n\nTesting project files...")
    print("-" * 50)
    
    required_files = [
        'main.py',
        'ui_main.py',
        'image_processor.py',
        'detector.py',
        'requirements.txt',
        'best_oto.pt'
    ]
    
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file:25} Found")
        else:
            print(f"✗ {file:25} Missing")
            missing.append(file)
    
    print("-" * 50)
    
    if missing:
        print(f"\n❌ {len(missing)} file(s) missing:")
        for file in missing:
            print(f"   - {file}")
        if 'best_oto.pt' in missing:
            print("\n⚠️  Model file 'best_oto.pt' is required!")
            print("   Please place your trained YOLO model in this directory.")
        return False
    else:
        print("\n✅ All required files found!")
        return True


def test_image_processor():
    """Test image processor module"""
    print("\n\nTesting image processor...")
    print("-" * 50)
    
    try:
        from image_processor import ImageProcessor
        import numpy as np
        
        processor = ImageProcessor()
        
        # Create a test image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Test enhancement
        enhanced = processor.enhance_image(
            test_image,
            clahe_clip=2.0,
            clahe_grid=(8, 8),
            gamma=1.0,
            brightness=0,
            contrast=1.0,
            denoise_strength=0
        )
        
        if enhanced is not None and enhanced.shape == test_image.shape:
            print("✓ Image enhancement works correctly")
            print("-" * 50)
            print("\n✅ Image processor test passed!")
            return True
        else:
            print("✗ Image enhancement failed")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        print("-" * 50)
        print("\n❌ Image processor test failed!")
        return False


def test_detector():
    """Test detector module"""
    print("\n\nTesting detector...")
    print("-" * 50)
    
    try:
        from detector import CarDetector
        import os
        
        if not os.path.exists('best_oto.pt'):
            print("⚠️  Model file 'best_oto.pt' not found")
            print("   Skipping detector test")
            print("-" * 50)
            return True
        
        detector = CarDetector('best_oto.pt')
        success = detector.load_model()
        
        if success:
            print("✓ YOLO model loaded successfully")
            print("-" * 50)
            print("\n✅ Detector test passed!")
            return True
        else:
            print("✗ Failed to load YOLO model")
            print("-" * 50)
            print("\n❌ Detector test failed!")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        print("-" * 50)
        print("\n❌ Detector test failed!")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Smart Traffic Car Counting System")
    print("Module Test Suite")
    print("=" * 50)
    
    results = []
    
    # Test imports
    results.append(("Module Imports", test_imports()))
    
    # Test files
    results.append(("Project Files", test_project_files()))
    
    # Test image processor
    results.append(("Image Processor", test_image_processor()))
    
    # Test detector
    results.append(("Detector", test_detector()))
    
    # Summary
    print("\n\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
    
    print("=" * 50)
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the application.")
        print("\nRun the application with:")
        print("   python main.py")
        print("   or double-click run.bat")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Ensure best_oto.pt is in the project directory")
        print("   3. Check Python version (3.8+ required)")
    
    print()


if __name__ == "__main__":
    main()
