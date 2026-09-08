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
logger = logging.getLogger("RobloxProBot")

# ==================== CONFIGURATION BLOCK ====================
ROBLOSECURITY_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyKAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0lWClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk"
GROUP_ID = 160052583  

ROLE_ID_1 = 832253071  
ROLE_ID_2 = 790162024  
ROLE_ID_3 = 793453002  

# Change this to your Group's base Rank ID (usually "Member" or "Guest" role ID)
ROLE_DEFAULT_MEMBER = 11637897572 

API_KEY_NAME = "X-API-Key"
API_SECRET_KEY = "MyPrivateSecretPassword123!"  

DB_FILE = "bot_audit_ledger.json"
# =============================================================

client = Client(ROBLOSECURITY_COOKIE)
app = FastAPI(title="Roblox Local Group Controller", version="3.0.0")

class DirectRoleRequest(BaseModel):
    user_id: int = Field(..., description="Target Roblox User ID")
    action: Literal["assign", "unassign"] = Field(..., description="Action context")
    target_role_id: Optional[int] = Field(None, description="Absolute Role ID")

def init_database():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"transactions": []}, f, indent=4)

def write_audit_log(user_id: int, action: str, role_id: Optional[int], execution_status: str, audit_message: str):
    init_database()
    with open(DB_FILE, "r+") as f:
        database = json.load(f)
        database["transactions"].append({
            "utc_timestamp": datetime.utcnow().isoformat(),
            "target_user_id": user_id,
            "requested_action": action,
            "applied_role_id": role_id,
            "status": execution_status,
            "meta_details": audit_message
        })
        f.seek(0)
        json.dump(database, f, indent=4)
        f.truncate()

async def validate_incoming_identity(api_key: str = Depends(APIKeyHeader(name=API_KEY_NAME, auto_error=True))):
    if api_key != API_SECRET_KEY:
        logger.warning(f"{Fore.RED}[SECURITY ALERT]{Style.RESET_ALL} Blocked unauthorized access attempt.")
        raise HTTPException(status_code=403, detail="Invalid global security token context.")
    return api_key

async def execute_roblox_api_mutation(user_id: int, action: str, selected_role_id: Optional[int] = None):
    try:
        group = await client.get_group(GROUP_ID)
        member = await group.get_member(user_id)
        
        if action == "assign":
            await member.set_role(selected_role_id)
            logger.info(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Assigned Role ID {selected_role_id} to User {user_id}")
            write_audit_log(user_id, action, selected_role_id, "SUCCESS", "Role successfully altered inside Roblox backend.")
            return {"status": "complete", "message": f"Successfully shifted user to role {selected_role_id}"}
            
        elif action == "unassign":
            await member.set_role(ROLE_DEFAULT_MEMBER)
            logger.info(f"{Fore.YELLOW}[SUCCESS]{Style.RESET_ALL} Flattened User {user_id} back to base role ID {ROLE_DEFAULT_MEMBER}")
            write_audit_log(user_id, action, ROLE_DEFAULT_MEMBER, "SUCCESS", "User demoted to base configuration rank.")
            return {"status": "complete", "message": f"Successfully dropped user to default track."}
            
    except Exception as e:
        error_dump = str(e)
        logger.error(f"{Fore.RED}[API FAULT]{Style.RESET_ALL} Processing failed for client: {error_dump}")
        write_audit_log(user_id, action, selected_role_id, "FAILED", error_dump)
        raise HTTPException(status_code=500, detail=f"Roblox platform integration fault: {error_dump}")

@app.post("/api/v3/group/modify", dependencies=[Depends(validate_incoming_identity)])
async def endpoint_process_group_change(payload: DirectRoleRequest):
    if payload.action == "assign":
        if not payload.target_role_id:
            raise HTTPException(status_code=400, detail="Missing parameter 'target_role_id'.")
        if payload.target_role_id not in [ROLE_ID_1, ROLE_ID_2, ROLE_ID_3]:
            raise HTTPException(status_code=400, detail="The specified Role ID is not registered in configuration.")
    
    logger.info(f"{Fore.CYAN}[REQ]{Style.RESET_ALL} Handling payload context for User {payload.user_id} -> Action: {payload.action}")
    execution_result = await execute_roblox_api_mutation(payload.user_id, payload.action, payload.target_role_id)
    return execution_result

@app.on_event("startup")
async def runtime_boot():
    init_database()
    logger.info(f"{Fore.MAGENTA}======================================================{Style.RESET_ALL}")
    logger.info(f"{Fore.MAGENTA}💎 PRIVATE LOCAL CORE ONLINE - LISTENING ON PORT 8000{Style.RESET_ALL}")
    logger.info(f"{Fore.MAGENTA}======================================================{Style.RESET_ALL}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
