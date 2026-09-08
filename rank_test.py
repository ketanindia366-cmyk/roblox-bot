import sys
import json
import urllib.request

API_URL = "http://127.0.0"
SECRET_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y"

def test_rank(target_user_id: int, action_type: str, role_id: int = None):
    payload = {
        "user_id": target_user_id,
        "action": action_type,
        "target_role_id": role_id
    }
    
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-API-Key": SECRET_KEY,
            "X-Source": "Terminal-Script" # Tells main.py to bypass the Roblox-Id header firewall gate safely
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            response_data = res.read().decode("utf-8")
            print(f"✅ Server Response: {response_data}")
    except Exception as e:
        print(f"❌ Failed to communicate with bot engine: {e}")

if __name__ == "__main__":
    print("--- 🛠️ ROBLOX BOT TERMINAL MANAGEMENT TOOL ---")
    user_input = input("Enter target Roblox User ID: ")
    action_input = input("Enter action (assign / unassign): ").strip().lower()
    
    role_input = None
    if action_input == "assign":
        print("\nAvailable Ranks:\n1 -> test (832253071)\n2 -> Tester (790162024)\n3 -> Lead Developer (793453002)")
        choice = input("Select rank number (1, 2, or 3): ").strip()
        role_map = {"1": 832253071, "2": 790162024, "3": 793453002}
        role_input = role_map.get(choice)
        
    test_rank(int(user_input), action_input, role_input)
