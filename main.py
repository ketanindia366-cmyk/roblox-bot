import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from colorama import Fore, Style, init
from roblox import Client

init(autoreset=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RobloxProAutomator")

# ==================== CONFIGURATION ENVIRONMENT ====================
ROBLOSECURITY_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyKAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0lWClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk"
GROUP_ID = 160052583  

ROLE_ID_1 = 832253071  
ROLE_ID_2 = 790162024  
ROLE_ID_3 = 793453002  

ROLE_DEFAULT_MEMBER = 12884901889 

API_KEY_NAME = "X-API-Key"
API_SECRET_KEY = "MyPrivateSecretPassword123!"  
DB_FILE = "bot_automation_ledger.json"
# ===================================================================

client = Client(ROBLOSECURITY_COOKIE)
app = FastAPI(title="Roblox Local Automation Matrix", version="4.0.0")

class AutomationRequest(BaseModel):
    user_id: int = Field(..., description="Roblox User Identifier Context")
    action: Literal["assign", "unassign"] = Field(..., description="Target manipulation mutation")
    target_role_id: Optional[int] = Field(None, description="Absolute group destination track")

def init_ledger():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"automated_events": []}, f, indent=4)

def commit_to_ledger(user_id: int, action: str, role_id: Optional[int], outcome: str, context: str):
    init_ledger()
    with open(DB_FILE, "r+") as f:
        data = json.load(f)
        data["automated_events"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "player_id": user_id,
            "action_executed": action,
            "role_mutated": role_id,
            "execution_status": outcome,
            "system_details": context
        })
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

async def verify_handshake(api_key: str = Depends(APIKeyHeader(name=API_KEY_NAME, auto_error=True))):
    if api_key != API_SECRET_KEY:
        logger.warning(f"{Fore.RED}[FIREWALL BLOCK]{Style.RESET_ALL} Rejected request signature.")
        raise HTTPException(status_code=403, detail="Unauthorized API payload credential configuration.")
    return api_key

async def process_roblox_group_change(user_id: int, action: str, group_role_id: Optional[int] = None):
    try:
        group = await client.get_group(GROUP_ID)
        member = await group.get_member(user_id)
        
        if action == "assign":
            await member.set_role(group_role_id)
            logger.info(f"{Fore.GREEN}[AUTO-PROMOTED]{Style.RESET_ALL} Shifted Player {user_id} -> Rank ID {group_role_id}")
            commit_to_ledger(user_id, action, group_role_id, "SUCCESS", "Automated system condition met.")
            return {"status": "success", "detail": f"Player {user_id} rank locked to {group_role_id}"}
            
        elif action == "unassign":
            await member.set_role(ROLE_DEFAULT_MEMBER)
            logger.info(f"{Fore.YELLOW}[AUTO-RESET]{Style.RESET_ALL} Cleaned data state for player {user_id}")
            commit_to_ledger(user_id, action, ROLE_DEFAULT_MEMBER, "SUCCESS", "Player configuration state reset.")
            return {"status": "success", "detail": "User rank returned to baseline default track."}
            
    except Exception as network_error:
        dump = str(network_error)
        logger.error(f"{Fore.RED}[ROBLOX FAULT]{Style.RESET_ALL} Mutation aborted: {dump}")
        commit_to_ledger(user_id, action, group_role_id, "FAILED", dump)
        raise HTTPException(status_code=500, detail=f"Target execution layer connection timeout: {dump}")

@app.post("/api/v4/automation/trigger", dependencies=[Depends(verify_handshake)])
async def intake_automation_event(payload: AutomationRequest):
    if payload.action == "assign":
        if not payload.target_role_id or payload.target_role_id not in [ROLE_ID_1, ROLE_ID_2, ROLE_ID_3]:
            raise HTTPException(status_code=400, detail="Invalid programmatic assignment rank requested.")
            
    logger.info(f"{Fore.CYAN}[ROUTING AUTO-EVENT]{Style.RESET_ALL} Player target: {payload.user_id} Context: {payload.action.upper()}")
    return await process_roblox_group_change(payload.user_id, payload.action, payload.target_role_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)