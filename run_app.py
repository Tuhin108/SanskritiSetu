"""
Simple script to run the Cultural Tourism Dashboard
No environment variables required for the sample data version
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'plotly', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("Packages installed successfully!")

def main():
    """Main function to run the app"""
    print("🎭 Starting India Cultural Heritage & Tourism Dashboard...")
    print("📊 Using sample data (no environment setup required)")
    
    # Check and install dependencies
    check_dependencies()
    
    # Run the Streamlit app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Thanks for exploring India's cultural heritage!")
    except Exception as e:
        print(f"Error running the app: {e}")

if __name__ == "__main__":
    main()
