import asyncio
import logging
import json
import os
import sys
import threading
import time
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from colorama import Fore, Style, init
from roblox import Client

init(autoreset=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RobloxSecurityMatrix")

# ==================== GROUP METADATA ENVIRONMENT ====================
ROBLOSECURITY_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyJAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0lWClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk"
GROUP_ID = 160052583  

ROLE_ID_1 = 832253071  # "test" Rank ID
ROLE_ID_2 = 790162024  # "Tester" Rank ID
ROLE_ID_3 = 793453002  # "Lead Developer • 🔨" Rank ID

ROLE_DEFAULT_MEMBER = 12884901889  # "Member" Base Rank ID

API_KEY_NAME = "X-API-Key"
API_SECRET_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y"  
QUEUE_FILE = "active_queue.json"
# ====================================================================

client = Client(ROBLOSECURITY_COOKIE)
app = FastAPI(title="Roblox Auto-Processing Core", version="5.0.0")
is_running = True

class AutomationRequest(BaseModel):
    user_id: int = Field(..., ge=1)
    action: Literal["assign", "unassign"]
    target_role_id: Optional[int] = Field(None, ge=0)

def init_queue():
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "w") as f:
            json.dump([], f)

def add_to_queue(user_id: int, action: str, role_id: Optional[int]):
    init_queue()
    with open(QUEUE_FILE, "r+") as f:
        data = json.load(f)
        if not any(item['user_id'] == user_id and item['action'] == action and item['role_id'] == role_id for item in data):
            data.append({"user_id": user_id, "action": action, "role_id": role_id, "timestamp": time.time()})
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

def pop_from_queue():
    init_queue()
    with open(QUEUE_FILE, "r+") as f:
        data = json.load(f)
        if not data:
            return None
        next_job = data.pop(0)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        return next_job

async def verify_handshake(request: Request, api_key: str = Depends(APIKeyHeader(name=API_KEY_NAME, auto_error=True))):
    if api_key != API_SECRET_KEY:
        logger.critical(f"{Fore.RED}[FIREWALL BLOCK]{Style.RESET_ALL} Invalid token.")
        raise HTTPException(status_code=403, detail="Access denied.")
    return api_key

async def process_job(user_id: int, action: str, group_role_id: Optional[int] = None):
    try:
        group = await client.get_group(GROUP_ID)
        member = await group.get_member(user_id)
        
        if action == "assign":
            await member.set_role(group_role_id)
            logger.info(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Ranked {user_id} to {group_role_id}")
        elif action == "unassign":
            await member.set_role(ROLE_DEFAULT_MEMBER)
            logger.info(f"{Fore.YELLOW}[RESET]{Style.RESET_ALL} Returned User {user_id} to Member.")
    except Exception as e:
        logger.error(f"{Fore.RED}[ROBLOX PLATFORM ERROR]{Style.RESET_ALL} {str(e)}")

def background_queue_runner():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    logger.info(f"{Fore.MAGENTA}⚡ AUTOMATED ENGINE ACTIVATED. PROCESSING LIVE DATA JOBS...{Style.RESET_ALL}")
    
    while is_running:
        job = pop_from_queue()
        if job:
            loop.run_until_complete(process_job(job["user_id"], job["action"], job["role_id"]))
        time.sleep(1)

@app.post("/api/v4/automation/trigger")
async def intake_automation_event(payload: AutomationRequest, api_key: str = Depends(verify_handshake)):
    if payload.action == "assign" and payload.target_role_id not in [ROLE_ID_1, ROLE_ID_2, ROLE_ID_3]:
        raise HTTPException(status_code=400, detail="Invalid rank mapping criteria requested.")
    
    add_to_queue(payload.user_id, payload.action, payload.target_role_id)
    return {"status": "queued"}

@app.on_event("startup")
async def startup_event():
    init_queue()
    threading.Thread(target=background_queue_runner, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    finally:
        is_running = False
        if os.path.exists(QUEUE_FILE):
            os.remove(QUEUE_FILE)
            print("🛑 App closed. Temporary live queue files scrubbed.")
