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
ROBLOSECURITY_COOKIE = "YOUR_BOT_ACCOUNT_ROBLOSECURITY_COOKIE_HERE"
GROUP_ID = 12345678  

ROLE_ID_1 = 11111111  
ROLE_ID_2 = 22222222  
ROLE_ID_3 = 33333333  
ROLE_DEFAULT_MEMBER = 00000000 

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
        logger.warning(f"{Fore.RED}[SECURITY ALERT]{Style.RESET_ALL} Blocked unauthorized key manipulation attempt.")
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
