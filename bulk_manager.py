# Save as bulk_manager.py
import asyncio
import urllib.request
import json

API_URL = "http://127.0.0"
SECRET_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y"
SOURCE_FILE = "bulk_queue.txt"

async def dispatch_rank_mutation(user_id: int, role_id: int):
    payload = {"user_id": user_id, "action": "assign", "target_role_id": role_id}
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-API-Key": SECRET_KEY},
        method="POST"
    )
    try:
        # Asynchronously drop requests onto your main app queue thread
        with urllib.request.urlopen(req) as res:
            print(f"✅ Dispatched bulk task for User {user_id} -> Rank {role_id}")
    except Exception as e:
        print(f"❌ Core engine rejected packet for user {user_id}: {e}")

async def process_bulk_file():
    print("📋 --- STARTING BULK AUTOMATION ENGINE MANAGEMENT --- 📋")
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ Error: Missing configuration data tracking file: {SOURCE_FILE}")
        return

    with open(SOURCE_FILE, "r") as file:
        tasks = []
        for line in file:
            if not line.strip() or "," not in line: continue
            uid, rank = line.strip().split(",")
            # Build an asynchronous task queue context execution stack
            tasks.append(dispatch_rank_mutation(int(uid), int(rank)))
            
        # Fire off all network requests simultaneously
        await asyncio.gather(*tasks)
    print("🏁 Bulk operations complete.")

if __name__ == "__main__":
    import os
    asyncio.run(process_bulk_file())
