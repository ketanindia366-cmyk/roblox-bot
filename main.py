import asyncio
import json
import logging
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from colorama import init, Fore, Style
from roblox import Client

# Initialize basic trace structures
init(autoreset=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ==================== CONFIGURATION ENVIRONMENT ====================
ROBLOSECURITY_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyJAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0lWClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk"
GROUP_ID = 160052583  

# Mapped natively to your exact group values
RANKS = {
    "test (832253071)": 832253071,
    "Tester (790162024)": 790162024,
    "Lead Developer (793453002)": 793453002
}
ROLE_DEFAULT_MEMBER = 12884901889  # Member (Base Rank ID)
# ====================================================================

# Initialize the Roblox client
roblox_client = Client(ROBLOSECURITY_COOKIE)

class RobloxBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Roblox Group Bot Control Dashboard")
        self.geometry("550x450")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)
        
        # Async loop for background tasks
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()
        
        self.setup_ui()
        self.log_message("🤖 System initialized. Ready to process changes.")
        
    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def setup_ui(self):
        # Header Label
        header = tk.Label(self, text="⚡ ROBLOX BOT DASHBOARD", font=("Arial", 16, "bold"), fg="#f1c40f", bg="#2c3e50")
        header.pack(pady=15)
        
        # User ID Frame
        uid_frame = tk.Frame(self, bg="#2c3e50")
        uid_frame.pack(pady=10)
        
        uid_label = tk.Label(uid_frame, text="Roblox User ID:", font=("Arial", 11), fg="#ecf0f1", bg="#2c3e50")
        uid_label.pack(side=tk.LEFT, padx=5)
        
        self.uid_entry = tk.Entry(uid_frame, font=("Arial", 11), width=20, bg="#34495e", fg="#white", insertbackground="white", bd=0)
        self.uid_entry.pack(side=tk.LEFT, padx=5)
        
        # Rank Selection Frame
        rank_frame = tk.Frame(self, bg="#2c3e50")
        rank_frame.pack(pady=10)
        
        rank_label = tk.Label(rank_frame, text="Select Rank:", font=("Arial", 11), fg="#ecf0f1", bg="#2c3e50")
        rank_label.pack(side=tk.LEFT, padx=5)
        
        self.rank_combo = ttk.Combobox(rank_frame, values=list(RANKS.keys()), state="readonly", width=25, font=("Arial", 10))
        self.rank_combo.set(list(RANKS.keys())[0])
        self.rank_combo.pack(side=tk.LEFT, padx=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#2c3e50")
        btn_frame.pack(pady=15)
        
        assign_btn = tk.Button(btn_frame, text="✅ ASSIGN RANK", font=("Arial", 10, "bold"), bg="#2ecc71", fg="white", width=15, command=self.trigger_assign, bd=0)
        assign_btn.pack(side=tk.LEFT, padx=10)
        
        unassign_btn = tk.Button(btn_frame, text="👋 RESET TO MEMBER", font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", width=18, command=self.trigger_unassign, bd=0)
        unassign_btn.pack(side=tk.LEFT, padx=10)
        
        # Logging Display Frame
        log_frame = tk.Frame(self, bg="#2c3e50")
        log_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        log_title = tk.Label(log_frame, text="Live Output Console:", font=("Arial", 10, "bold"), fg="#95a5a6", bg="#2c3e50")
        log_title.pack(anchor="w")
        
        self.log_box = tk.Text(log_frame, height=10, bg="#1e272e", fg="#00d2d3", font=("Courier", 10), state=tk.DISABLED, bd=0)
        self.log_box.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def log_message(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {text}\n"
        
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, formatted)
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)

    def get_validated_uid(self):
        uid_str = self.uid_entry.get().strip()
        if not uid_str.isdigit():
            messagebox.showerror("Validation Error", "Please provide a valid, numeric Roblox User ID.")
            return None
        return int(uid_str)

    def trigger_assign(self):
        uid = self.get_validated_uid()
        if not uid: return
        
        selected_rank_name = self.rank_combo.get()
        target_role_id = RANKS[selected_rank_name]
        
        self.log_message(f"⌛ Queued task: Assign user {uid} to {selected_rank_name}...")
        asyncio.run_coroutine_threadsafe(self.execute_mutation(uid, "assign", target_role_id), self.loop)

    def trigger_unassign(self):
        uid = self.get_validated_uid()
        if not uid: return
        
        self.log_message(f"⌛ Queued task: Demote user {uid} to Base Member...")
        asyncio.run_coroutine_threadsafe(self.execute_mutation(uid, "unassign", ROLE_DEFAULT_MEMBER), self.loop)

    async def execute_mutation(self, user_id: int, action: str, role_id: int):
        try:
            group = await roblox_client.get_group(GROUP_ID)
            member = await group.get_member(user_id)
            
            await member.set_role(role_id)
            
            if action == "assign":
                self.after(0, lambda: self.log_message(f"🎉 SUCCESS: Ranked User ID {user_id} successfully!"))
            else:
                self.after(0, lambda: self.log_message(f"🧹 SUCCESS: Reset User ID {user_id} back to Member tracker."))
                
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self.log_message(f"❌ ERROR: Transaction rejected. Detail: {err_msg}"))

if __name__ == "__main__":
    app = RobloxBotApp()
    app.mainloop()
