import asyncio
import logging
import json
import os
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

# ==================== SECURE PRODUCTION BLOCK ====================
ROBLOSECURITY_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyKAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0lWClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk"
GROUP_ID = 160052583  

ROLE_ID_1 = 832253071  # "test" Rank
ROLE_ID_2 = 790162024  # "Tester" Rank
ROLE_ID_3 = 793453002  # "Lead Developer" Rank

ROLE_DEFAULT_MEMBER = 12884901889  # "Member" Base Rank

API_KEY_NAME = "X-API-Key"
API_SECRET_KEY = "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y"  
DB_FILE = "secure_automation_ledger.json"
# =================================================================

client = Client(ROBLOSECURITY_COOKIE)
app = FastAPI(title="Roblox Hardened Security Core", version="5.0.0")

class AutomationRequest(BaseModel):
    user_id: int = Field(..., ge=1)
    action: Literal["assign", "unassign"]
    target_role_id: Optional[int] = Field(None, ge=0)

def init_ledger():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"secured_transactions": []}, f, indent=4)

def commit_to_ledger(user_id: int, action: str, role_id: Optional[int], outcome: str, context: str):
    init_ledger()
    try:
        with open(DB_FILE, "r+") as f:
            data = json.load(f)
            data["secured_transactions"].append({
                "timestamp_utc": datetime.utcnow().isoformat(),
                "validated_player_id": user_id,
                "action": action,
                "role_id_applied": role_id,
                "status": outcome,
                "audit_meta": context
            })
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception:
        pass

async def verify_hardened_handshake(request: Request, api_key: str = Depends(APIKeyHeader(name=API_KEY_NAME, auto_error=True))):
    if api_key != API_SECRET_KEY:
        logger.critical(f"{Fore.RED}[FIREWALL BLOCK]{Style.RESET_ALL} Rejected invalid authorization signature.")
        raise HTTPException(status_code=403, detail="Access denied. Invalid token context.")
    
    # Internal bypass for the terminal script file, otherwise check Roblox origin headers
    roblox_header = request.headers.get("Roblox-Id")
    user_agent = request.headers.get("user-agent", "")
    is_terminal = request.headers.get("X-Source") == "Terminal-Script"
    
    if not roblox_header and "Roblox" not in user_agent and not is_terminal:
        logger.critical(f"{Fore.RED}[SPOOF WARNING]{Style.RESET_ALL} Request blocked. Source didn't originate from a Roblox server instance.")
        raise HTTPException(status_code=403, detail="Access denied. Context tracking parameters missing.")
        
    return api_key

async def execute_roblox_api_mutation(user_id: int, action: str, group_role_id: Optional[int] = None):
    try:
        group = await client.get_group(GROUP_ID)
        member = await group.get_member(user_id)
        
        if action == "assign":
            await member.set_role(group_role_id)
            logger.info(f"{Fore.GREEN}[SECURE SUCCESS]{Style.RESET_ALL} Automated group alignment complete for: {user_id}")
            commit_to_ledger(user_id, action, group_role_id, "SUCCESS", "Passed all structural firewall gates safely.")
            return {"status": "success", "detail": f"Locked user target context to role layout {group_role_id}"}
            
        elif action == "unassign":
            await member.set_role(ROLE_DEFAULT_MEMBER)
            logger.info(f"{Fore.YELLOW}[SECURE RESET]{Style.RESET_ALL} Successfully reset configuration mapping track for: {user_id}")
            commit_to_ledger(user_id, action, ROLE_DEFAULT_MEMBER, "SUCCESS", "Demoted back to fallback state configuration context.")
            return {"status": "success", "detail": "User context tracking successfully rolled back."}
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"{Fore.RED}[PLATFORM FAULT]{Style.RESET_ALL} Rejection encountered from backend API: {error_msg}")
        commit_to_ledger(user_id, action, group_role_id, "FAILED", error_msg)
        raise HTTPException(status_code=500, detail="Internal connection issue between bot and Roblox backend.")

@app.post("/api/v4/automation/trigger", dependencies=[Depends(verify_hardened_handshake)])
async def intake_automation_event(payload: AutomationRequest):
    if payload.action == "assign":
        if not payload.target_role_id or payload.target_role_id not in [ROLE_ID_1, ROLE_ID_2, ROLE_ID_3]:
            raise HTTPException(status_code=400, detail="Injection tracking blocked. Specified role destination is illegal.")
            
    return await execute_roblox_api_mutation(payload.user_id, payload.action, payload.target_role_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
