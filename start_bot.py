import os
import sys
import subprocess

# List of all required libraries for your pro bot
REQUIRED_LIBRARIES = ["roblox", "fastapi", "uvicorn", "pydantic", "colorama"]

def setup_and_launch():
    print("🤖 --- ROBLOX AUTO-RANK BOOT ENGINE --- 🤖\n")
    
    # 1. Automatically check and install dependencies (Skipped if already installed)
    print("🔍 Checking system dependencies...")
    for library in REQUIRED_LIBRARIES:
        try:
            __import__(library)
        except ImportError:
            print(f"📦 Missing '{library}'. Installing automatically via pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            
    print("✅ All dependencies verified and ready!\n")
    
    # 2. Verify that main.py exists in the folder
    if not os.path.exists("main.py"):
        print("❌ CRITICAL ERROR: Could not find 'main.py' in this folder!")
        print("Please make sure this script is saved in the same directory as your main bot file.")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    print("🚀 Launching Roblox Hardened Security Core on http://127.0.0.1:8000 ...")
    print("----------------------------------------------------------------------")
    
    # 3. Boot up the main server script smoothly
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n🛑 Bot server shut down safely.")

if __name__ == "__main__":
    setup_and_launch()
