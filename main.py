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
import webbrowser
import winsound

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ==================== CONFIGURATION ENVIRONMENT ====================
RANKS = {
    "test (832253071)": 832253071,
    "Tester (790162024)": 790162024,
    "Lead Developer (793453002)": 793453002
}
ROLE_DEFAULT_MEMBER = 12884901889  
AUTH_FILE = "user_auth.json"
HTML_DASHBOARD = "index.html"
NODE_SERVER_FILE = "server.js"

COLOR_BG = "#1e1e2e"       
COLOR_PANEL = "#252538"    
COLOR_TEXT = "#cdd6f4"     
COLOR_ACCENT = "#cba6f7"   
COLOR_GREEN = "#a6e3a1"    
COLOR_RED = "#f38ba8"      
# ====================================================================

class AnimatedBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Roblox Unified Control Framework")
        self.geometry("700x560") 
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)
        
        self.sidebar_open = False
        self.sidebar_width = 200
        
        self.setup_styles()
        self.is_authenticated = False
        self.build_auth_screen()
        
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
            messagebox.showerror("Auth Failure", "Please enter a valid email.")
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
            messagebox.showerror("Auth Error", "No credentials located. Sign up first.")
            return
        with open(AUTH_FILE, "r") as f:
            stored_data = json.load(f)
        if email == stored_data["registered_email"] and self.hash_password(password) == stored_data["password_hash"]:
            self.is_authenticated = True
            self.auth_frame.destroy()
            
            # Start node server and open web page instantly on login
            subprocess.Popen(["node", NODE_SERVER_FILE], shell=True)
            if os.path.exists(HTML_DASHBOARD):
                webbrowser.open(os.path.abspath(HTML_DASHBOARD))
                
            self.build_main_dashboard()
        else:
            messagebox.showerror("Auth Error", "Access Denied.")

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
        
        self.menu_btn = tk.Button(self.top_bar, text="📋 App Logs", font=("Arial", 11, "bold"), bg=COLOR_PANEL, fg=COLOR_ACCENT, bd=0, activebackground=COLOR_BG, activeforeground=COLOR_TEXT, command=self.toggle_sidebar)
        self.menu_btn.pack(side=tk.LEFT, padx=15)
        
        title_lbl = tk.Label(self.top_bar, text="UNIFIED NODE & PYTHON GATEWAY", font=("Arial", 11, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        title_lbl.pack(side=tk.LEFT, padx=10)
        
        self.main_container = tk.Frame(self, bg=COLOR_BG)
        self.main_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.logo_canvas = tk.Canvas(self.main_container, width=80, height=80, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.logo_canvas.pack(pady=(5, 5))
        self.logo_canvas.create_polygon(40, 5, 75, 20, 75, 55, 40, 75, 5, 55, 5, 20, fill=COLOR_PANEL, outline=COLOR_ACCENT, width=2)
        self.logo_canvas.create_text(40, 40, text="🌐", font=("Arial", 22), fill=COLOR_TEXT)
        
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
        
        self.bar_lbl = tk.Label(self.card, text="Ecosystem Idle", font=("Arial", 9, "bold"), fg="#95a5a6", bg=COLOR_PANEL)
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
        
        side_title = tk.Label(self.sidebar, text="Ecosystem Terminal", font=("Arial", 11, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        side_title.pack(pady=10, anchor="w", padx=15)
        
        self.log_box = tk.Text(self.sidebar, bg=COLOR_BG, fg=COLOR_TEXT, font=("Courier", 9), state=tk.DISABLED, bd=0, wrap=tk.WORD)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.log_message("⚡ Link established. Cross-language server loops online.")

    def animate_progress_bar(self, target_percentage: int, label_text: str, fill_color: str):
        def step_fill(current_pct):
            if current_pct > target_percentage:
                if target_percentage == 100:
                    self.bar_lbl.config(text="🎉 Action Finalized", fg=COLOR_GREEN)
