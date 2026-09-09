# Save as start_bot.py
import os
import sys
import subprocess

REQUIRED_LIBRARIES = ["roblox", "fastapi", "uvicorn", "pydantic", "colorama"]

def setup_and_launch():
    print("🤖 --- ROBLOX ENTERPRISE SYSTEM INITIALIZER --- 🤖\n")
    print("🔍 Inspecting system environment core libraries...")
    
    for library in REQUIRED_LIBRARIES:
        try:
            __import__(library)
        except ImportError:
            print(f"📦 Library '{library}' not found. Initializing silent deployment update...")
            subprocess.check_call(["py", "-m", "pip", "install", library, "--no-cache-dir", "--disable-pip-version-check"])
            
    print("✅ System modules verified successfully!\n")
    
    if not os.path.exists("main.py"):
        print("❌ CRITICAL BOOT ERROR: 'main.py' is missing from this workspace file block.")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    print("🚀 Mounting Main Interface Dashboard Window...")
    print("----------------------------------------------------------------------")
    
    try:
        subprocess.run(["py", "main.py"])
    except KeyboardInterrupt:
        print("\n🛑 Execution sequence terminated safely by administrator.")

if __name__ == "__main__":
    setup_and_launch()
