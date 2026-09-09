import asyncio
import json
import logging
import os
import sys
import subprocess
import hashlib
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import winsound

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ==================== CONFIGURATION ENVIRONMENT ====================
ROBLOSECURITY_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEQAhoGCAIQBBgBIhwKBGR1aWQSFDEyMTY5MTMxNDMwNTU0MTI3ODk2IhQKBXVuYW1lEgtBbGllbnNFdmVudCISCgN1aWQSCzExNjM3ODk3NTcyJAM.bS6F_z94WoemgVBMo7N7EBwxeut_uH_c_IUE-mTDbC9JBAqX6oeK7qrkdhaBt64LFcpd0n36Nj2aSgrXSk5YyoHm6ogoD9w7IGjaXCFbI5I0i9PW4lkoAXe6wvjrJccEBf7soChGRcqAIMxDuNh__xXJ4SyDozRkETnMXkqjjSuKRyi4f7gsAxRU_-RKSBCMBwiXG6eE4rDk3QJXwMYgc0Zf1-YN6u-rsKOS-bu0brYi3if_h3efxOoXUEaKS6l4tcllppbVl_SbMqBl8PWr-xN55MuHOpu9IBBsat_mwvt8WBvtufhSNnTWIkRNkjrKmwVLDuFTY0c2FTrcvE48UhTDXlf2QZI1-U58RyhPBz-vnsOAwc8th92w3esF1vHaem2VVtZWk1pKe7-rU72Oz6weDNqO_zN__VOvB1WX51iAaz6e-nlLuHeEyIMTo4zw9rykQtLkdZptrSAGQXxtWidv6xWp_TWw7LhlazK3V53uWUhG54wRChRcseEF2SgKXyDBOwMvXOlAn985w-6LX9PB_bu_8BBB0CklNdLFkRgJewukffc8YTDX309Of6zz17ucKXRob3nlt252qUPKK9EiQ-y3sk9nWKo012YA5_wTplR1wfqZh5Wj4TFPgOTrsxBSC4RdsWyUoe8r_7Tv9CCY7sSGx_V3QtFxZYrgw8M06D09E174cZKHRPYt6dpGjkF_s2MaD7_A6LDd8bTEh0NFmXwB2DLZo4SjxJc9lXG8Sgcc_eHu3cjA09sJjEwdFgnHF5vewgXitlk6Kv-6CtsZuZB5S191sSJvBrHEcxExq0WClSUpgAdreQvB5M0N845WilZH31Zm6Dz-ztqNHRGrn60il7cmKRLtEiWI3HT_6OnrKYjU1cFkVZYH1JQnBpfdm-UMpmvuC_vSF8oYk6JCFYMPAjkiEcQAyysmig.mCDwiKSyzmqA5yRilB_fWAAxBkk"
GROUP_ID = 160052583  

RANKS = {
    "test (832253071)": 832253071,
    "Tester (790162024)": 790162024,
    "Lead Developer (793453002)": 793453002
}
ROLE_DEFAULT_MEMBER = 12884901889  
JAVA_JAR_FILE = "roblox_helper.jar" 
AUTH_FILE = "user_auth.json"
ICON_FILE = "app_logo.ico"

# Palette UI Themes
COLOR_BG = "#1e1e2e"       
COLOR_PANEL = "#252538"    
COLOR_TEXT = "#cdd6f4"     
COLOR_ACCENT = "#cba6f7"   
COLOR_GREEN = "#a6e3a1"    
COLOR_RED = "#f38ba8"      
# ====================================================================

try:
    from roblox import Client
    roblox_client = Client(ROBLOSECURITY_COOKIE)
except ImportError:
    roblox_client = None

class AnimatedBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Roblox System Gatekeeper Engine")
        self.geometry("700x560") 
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)
        
        if os.path.exists(ICON_FILE):
            try:
                self.iconbitmap(ICON_FILE)
            except Exception:
                pass
        
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()
        
        self.sidebar_open = False
        self.sidebar_width = 200
        
        self.setup_styles()
        self.is_authenticated = False
        
        self.build_auth_screen()
        
    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=COLOR_PANEL, background=COLOR_BG, foreground=COLOR_TEXT, arrowcolor=COLOR_ACCENT, bordercolor=COLOR_BG)
        style.map("TCombobox", fieldbackground=[("readonly", COLOR_PANEL)], foreground=[("readonly", COLOR_TEXT)])

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_signup(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not email or "@" not in email or not password:
            messagebox.showerror("Auth Failure", "Please enter a valid email structure.")
            return
        if os.path.exists(AUTH_FILE):
            messagebox.showerror("Auth Failure", "An account is already registered.")
            return
        auth_payload = {"registered_email": email, "password_hash": self.hash_password(password)}
        with open(AUTH_FILE, "w") as f:
            json.dump(auth_payload, f, indent=4)
        messagebox.showinfo("Success", "Account created successfully.")
        self.auth_frame.destroy()
        self.build_auth_screen()

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not os.path.exists(AUTH_FILE):
            messagebox.showerror("Auth Error", "No credentials file located. Sign up first.")
            return
        with open(AUTH_FILE, "r") as f:
            stored_data = json.load(f)
        if email == stored_data["registered_email"] and self.hash_password(password) == stored_data["password_hash"]:
            self.is_authenticated = True
            self.auth_frame.destroy()
            self.build_main_dashboard()
        else:
            messagebox.showerror("Auth Error", "Access Denied. Credentials mismatched.")

    def build_auth_screen(self):
        self.auth_frame = tk.Frame(self, bg=COLOR_BG)
        self.auth_frame.pack(fill=tk.BOTH, expand=True)
        has_account = os.path.exists(AUTH_FILE)
        title_text = "PORTAL GATE: LOGIN" if has_account else "PORTAL GATE: SIGN UP"
        
        header = tk.Label(self.auth_frame, text=title_text, font=("Arial", 16, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG)
        header.pack(pady=40)
        
        card = tk.Frame(self.auth_frame, bg=COLOR_PANEL, width=400, height=260, highlightbackground="#313244", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        card.pack_propagate(False)
        
        tk.Label(card, text="Account Email Address", font=("Arial", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(pady=(20, 5), anchor="w", padx=40)
        self.email_entry = tk.Entry(card, font=("Arial", 11), width=32, bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0, highlightthickness=1, highlightbackground="#313244", highlightcolor=COLOR_ACCENT)
        self.email_entry.pack(pady=5, ipady=3)
        
        tk.Label(card, text="Security Password", font=("Arial", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(pady=(10, 5), anchor="w", padx=40)
        self.pass_entry = tk.Entry(card, show="*", font=("Arial", 11), width=32, bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0, highlightthickness=1, highlightbackground="#313244", highlightcolor=COLOR_ACCENT)
        self.pass_entry.pack(pady=5, ipady=3)
        
        if has_account:
            login_btn = tk.Button(card, text="Authenticate Now", font=("Arial", 10, "bold"), bg=COLOR_GREEN, fg=COLOR_BG, bd=0, cursor="hand2", width=20, command=self.handle_login)
            login_btn.pack(pady=20, ipady=4)
        else:
            signup_btn = tk.Button(card, text="Register Credentials", font=("Arial", 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG, bd=0, cursor="hand2", width=20, command=self.handle_signup)
            signup_btn.pack(pady=20, ipady=4)

    def build_main_dashboard(self):
        self.top_bar = tk.Frame(self, bg=COLOR_PANEL, height=50)
        self.top_bar.pack(fill=tk.X)
        self.top_bar.pack_propagate(False)
        
        self.menu_btn = tk.Button(self.top_bar, text="☰ Logs", font=("Arial", 11, "bold"), bg=COLOR_PANEL, fg=COLOR_ACCENT, bd=0, activebackground=COLOR_BG, activeforeground=COLOR_TEXT, command=self.toggle_sidebar)
        self.menu_btn.pack(side=tk.LEFT, padx=15)
        
        title_lbl = tk.Label(self.top_bar, text="ROBLOX SECURITY AUTOMATION HUD", font=("Arial", 12, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        title_lbl.pack(side=tk.LEFT, padx=10)
        
        self.main_container = tk.Frame(self, bg=COLOR_BG)
        self.main_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.logo_canvas = tk.Canvas(self.main_container, width=80, height=80, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.logo_canvas.pack(pady=(5, 5))
        self.logo_canvas.create_polygon(40, 5, 75, 20, 75, 55, 40, 75, 5, 55, 5, 20, fill=COLOR_PANEL, outline=COLOR_ACCENT, width=2)
        self.logo_canvas.create_text(40, 40, text="🤖", font=("Arial", 22), fill=COLOR_TEXT)
        
        self.card = tk.Frame(self.main_container, bg=COLOR_PANEL, width=420, height=330, highlightbackground="#313244", highlightthickness=1)
        self.card.pack(pady=5)
        self.card.pack_propagate(False)
        
        uid_lbl = tk.Label(self.card, text="Target Player User ID", font=("Arial", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        uid_lbl.pack(pady=(15, 3), anchor="w", padx=40)
        
        self.uid_entry = tk.Entry(self.card, font=("Arial", 12), width=34, bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0, highlightthickness=1, highlightbackground="#313244", highlightcolor=COLOR_ACCENT)
        self.uid_entry.pack(pady=2, ipady=4)
        
        rank_lbl = tk.Label(self.card, text="Destination Group Rank", font=("Arial", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        rank_lbl.pack(pady=(10, 3), anchor="w", padx=40)
        
        self.rank_combo = ttk.Combobox(self.card, values=list(RANKS.keys()), state="readonly", width=36, font=("Arial", 11))
        self.rank_combo.set(list(RANKS.keys()))
        self.rank_combo.pack(pady=2)
        
        self.bar_lbl = tk.Label(self.card, text="Network Transit Idle", font=("Arial", 9, "bold"), fg="#95a5a6", bg=COLOR_PANEL)
        self.bar_lbl.pack(pady=(15, 2), anchor="w", padx=40)
        
        self.bar_canvas = tk.Canvas(self.card, width=340, height=14, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.bar_canvas.pack(pady=2)
        self.bar_canvas.create_rectangle(0, 0, 340, 14, fill="#181825", width=0, tags="track")
        
        btn_frame = tk.Frame(self.card, bg=COLOR_PANEL)
        btn_frame.pack(pady=20, fill=tk.X, padx=40)
                self.assign_btn = tk.Button(btn_frame, text="Assign Rank", font=("Arial", 10, "bold"), bg=COLOR_GREEN, fg=COLOR_BG, bd=0, cursor="hand2", width=14, command=self.trigger_assign)
        self.assign_btn.pack(side=tk.LEFT, ipady=6)
        self.setup_hover_effect(self.assign_btn, COLOR_GREEN, "#b4befe")

        self.reset_btn = tk.Button(btn_frame, text="Reset Member", font=("Arial", 10, "bold"), bg=COLOR_RED, fg=COLOR_BG, bd=0, cursor="hand2", width=14, command=self.trigger_unassign)
        self.reset_btn.pack(side=tk.RIGHT, ipady=6)
        self.setup_hover_effect(self.reset_btn, COLOR_RED, "#f5e0dc")

        self.sidebar = tk.Frame(self, bg=COLOR_PANEL, width=0, highlightbackground="#313244", highlightthickness=1)
        self.sidebar.place(x=-self.sidebar_width, y=50, height=510)
        self.sidebar.pack_propagate(False)

        side_title = tk.Label(self.sidebar, text="Transaction Logs", font=("Arial", 11, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        side_title.pack(pady=10, anchor="w", padx=15)

        self.log_box = tk.Text(self.sidebar, bg=COLOR_BG, fg=COLOR_TEXT, font=("Courier", 9), state=tk.DISABLED, bd=0, wrap=tk.WORD)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.log_message("⚡ Secure Shell Handshake Initialized. Ready to process records.")

    def animate_progress_bar(self, target_percentage: int, label_text: str, fill_color: str):
        def step_fill(current_pct):
            if current_pct > target_percentage:
                if target_percentage == 100:
                    self.bar_lbl.config(text="🎉 Process Finalized", fg=COLOR_GREEN)
                    threading.Thread(target=lambda: winsound.MessageBeep(winsound.MB_ICONASTERISK), daemon=True).start()
                    self.after(1500, lambda: self.reset_progress_bar())
                return
            
            pixel_width = int((current_pct / 100) * 340)
            self.bar_canvas.delete("fill_chunk")
            self.bar_canvas.create_rectangle(0, 0, pixel_width, 14, fill=fill_color, width=0, tags="fill_chunk")
            self.bar_lbl.config(text=f"⚡ {label_text}: {current_pct}%", fg=COLOR_ACCENT)
            self.update_idletasks()
            self.after(8, lambda: step_fill(current_pct + 2))
            
        step_fill(0)

    def reset_progress_bar(self):
        self.bar_canvas.delete("fill_chunk")
        self.bar_lbl.config(text="Network Transit Idle", fg="#95a5a6")

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.animate_sidebar(-self.sidebar_width, False)
        else:
            self.animate_sidebar(0, True)

    def animate_sidebar(self, target_x, target_state):
        def loop_step(current_x):
            step = 25 if target_x > current_x else -25
            next_x = current_x + step
            if (step > 0 and next_x >= target_x) or (step < 0 and next_x <= target_x):
                self.sidebar.place(x=target_x, width=self.sidebar_width)
                self.sidebar_open = target_state
                return
            self.sidebar.place(x=next_x, width=self.sidebar_width)
            self.update_idletasks()
            self.after(10, lambda: loop_step(next_x))
        start_x = int(self.sidebar.place_info()["x"])
        loop_step(start_x)

    def setup_hover_effect(self, widget, color_base, color_hover):
        # FIX: Restored missing Enter/Leave strings so Tkinter reads mouse movement
        widget.bind("<Enter>", lambda e: widget.config(bg=color_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=color_base))

    def log_message(self, text):
        if not hasattr(self, 'log_box'): return
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
        
        self.animate_progress_bar(100, "Encrypting Handshake & Mutating Rank", COLOR_GREEN)
        self.log_message(f"⌛ Queued task: Move user {uid} to {selected_rank_name}...")
        asyncio.run_coroutine_threadsafe(self.execute_mutation(uid, "assign", target_role_id), self.loop)
        self.run_java_companion(uid, "assign", target_role_id)

    def trigger_unassign(self):
        uid = self.get_validated_uid()
        if not uid: return
        
        self.animate_progress_bar(100, "Clearing Node Context & Flattening", COLOR_RED)
        self.log_message(f"⌛ Queued task: Reset user {uid} back to baseline community rank...")
        asyncio.run_coroutine_threadsafe(self.execute_mutation(uid, "unassign", ROLE_DEFAULT_MEMBER), self.loop)
        self.run_java_companion(uid, "unassign", ROLE_DEFAULT_MEMBER)

    async def execute_mutation(self, user_id: int, action: str, role_id: int):
        if not roblox_client:
            await asyncio.sleep(1) 
            self.after(0, lambda: self.log_message(f"✨ Mock Trace Success: Manipulated target matching ID {user_id}"))
            return
        try:
            group = await roblox_client.get_group(GROUP_ID)
            member = await group.get_member(user_id)
            await member.set_role(role_id)
            if action == "assign":
                self.after(0, lambda: self.log_message(f"🎉 API Mutation Confirmed: Swapped rank fields for target user {user_id}."))
            else:
                self.after(0, lambda: self.log_message(f"🧹 API Mutation Confirmed: Returned user tracking matrix {user_id} to member track."))
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self.log_message(f"❌ Network core error encountered: {err_msg}"))

    def run_java_companion(self, user_id, action, rank_id):
        if not os.path.exists(JAVA_JAR_FILE): return
        def run():
            try:
                cmd = ["java", "-jar", JAVA_JAR_FILE, str(user_id), str(action), str(rank_id)]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.after(0, lambda: self.log_message(f"☕ [Java Ledger Data Recieved]: {res.stdout.strip()}"))
            except Exception:
                pass
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    # FIX: Corrected variable format from if name == "main":
    app = AnimatedBotApp()
    app.mainloop()

