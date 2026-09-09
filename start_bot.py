import os
import sys
import subprocess

REQUIRED_LIBRARIES = ["roblox", "fastapi", "uvicorn", "pydantic", "colorama"]

def setup_and_launch():
    print("🤖 --- ROBLOX DESKTOP APP ENGINE BOOTER --- 🤖\n")
    print("🔍 Verifying system environment libraries...")
    
    for library in REQUIRED_LIBRARIES:
        try:
            __import__(library)
        except ImportError:
            print(f"📦 Missing library '{library}'. Installing automatically...")
            # Bypasses Windows Environment PATH bugs cleanly using 'py'
            subprocess.check_call(["py", "-m", "pip", "install", library, "--no-cache-dir", "--disable-pip-version-check"])
            
    print("✅ All system dependencies verified and ready!\n")
    
    if not os.path.exists("main.py"):
        print("❌ CRITICAL ERROR: Could not find 'main.py' in this folder!")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    print("🚀 Launching Master Automation Core Dashboard...")
    print("----------------------------------------------------------------------")
    
    try:
        subprocess.run(["py", "main.py"])
    except KeyboardInterrupt:
        print("\n🛑 Bot engine shut down safely.")

if __name__ == "__main__":
    setup_and_launch()
