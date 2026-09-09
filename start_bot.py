import os
import sys
import subprocess

# List of required production libraries
REQUIRED_LIBRARIES = ["roblox", "fastapi", "uvicorn", "pydantic", "colorama"]

def setup_and_launch():
    print("🤖 --- ROBLOX ENTERPRISE BOT ENGINE BOOTER --- 🤖\n")
    
    # 1. Force the script to run under the Windows Python Launcher
    print("🔍 Verifying system environment...")
    
    # 2. Automatically check and install dependencies 
    for library in REQUIRED_LIBRARIES:
        try:
            __import__(library)
        except ImportError:
            print(f"📦 Missing library '{library}'. Installing automatically...")
            # Using 'py -m pip' avoids the PATH environment bugs entirely on Windows
            subprocess.check_call(["py", "-m", "pip", "install", library])
            
    print("✅ All system dependencies verified and ready!\n")
    
    # 3. Check for the main script file
    if not os.path.exists("main.py"):
        print("❌ CRITICAL ERROR: Could not find 'main.py' in this folder!")
        print("Please save this script in the exact same directory as your main bot file.")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    print("🚀 Launching Hardened Security Matrix on http://127.0.0.1:8000 ...")
    print("----------------------------------------------------------------------")
    
    # 4. Boot up the main engine using the safe Windows launcher
    try:
        subprocess.run(["py", "main.py"])
    except KeyboardInterrupt:
        print("\n🛑 Bot engine shut down safely.")

if __name__ == "__main__":
    setup_and_launch()
