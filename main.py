# Save as main.py
import asyncio
import json
import os
import sys
import subprocess
import hashlib
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import webbrowser

from app_gui import AppGUI, COLOR_BG, COLOR_PANEL, COLOR_TEXT, COLOR_ACCENT, COLOR_GREEN, COLOR_RED

RANKS = {
    "test (832253071)": 832253071,
    "Tester (790162024)": 790162024,
    "Lead Developer (793453002)": 793453002
}
ROLE_DEFAULT_MEMBER = 12884901889  
AUTH_FILE = "user_auth.json"
HTML_DASHBOARD = "index.html"
NODE_SERVER_FILE = "server.js"
JAVA_JAR_FILE = "roblox_helper.jar"

class AnimatedBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Roblox Unified Control Framework")
        self.geometry("700x560") 
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)
        
        self.ranks = RANKS
        self.sidebar_open = False
        self.sidebar_width = 200
        
        self.gui_builder = AppGUI(self)
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=lambda: self.loop.run_forever(), daemon=True).start()
        
        self.gui_builder.app.setup_styles()
        self.build_auth_screen()

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_signup(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not email or "@" not in email or not password:
            messagebox.showerror("Auth Failure", "Please enter a valid email.")
            return
        with open(AUTH_FILE, "w") as f:
            json.dump({"registered_email": email, "password_hash": self.hash_password(password)}, f, indent=4)
        messagebox.showinfo("Success", "Account created successfully.")
        self.auth_frame.destroy()
        self.build_auth_screen()

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not os.path.exists(AUTH_FILE): return
        with open(AUTH_FILE, "r") as f:
            stored = json.load(f)
        if email == stored["registered_email"] and self.hash_password(password) == stored["password_hash"]:
            self.auth_frame.destroy()
            subprocess.Popen(["node", NODE_SERVER_FILE], shell=True)
            if os.path.exists(HTML_DASHBOARD): webbrowser.open(os.path.abspath(HTML_DASHBOARD))
            self.gui_builder.build_main_dashboard()
        else:
            messagebox.showerror("Auth Error", "Access Denied.")

    def build_auth_screen(self):
        self.auth_frame = tk.Frame(self, bg=COLOR_BG)
        self.auth_frame.pack(fill=tk.BOTH, expand=True)
        has_account = os.path.exists(AUTH_FILE)
        
        tk.Label(self.auth_frame, text="PORTAL GATE" if has_account else "SIGN UP", font=("Arial", 16, "bold"), fg=COLOR_ACCENT, bg=COLOR_BG).pack(pady=40)
        card = tk.Frame(self.auth_frame, bg=COLOR_PANEL, width=400, height=260, highlightbackground="#313244", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        card.pack_propagate(False)
        
        tk.Label(card, text="Email Address", font=("Arial", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(pady=(20, 5), anchor="w", padx=40)
        self.email_entry = tk.Entry(card, font=("Arial", 11), width=32, bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0)
        self.email_entry.pack(pady=5, ipady=3)
        
        tk.Label(card, text="Password", font=("Arial", 10, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL).pack(pady=(10, 5), anchor="w", padx=40)
        self.password_entry = tk.Entry(card, show="*", font=("Arial", 11), width=32, bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0)
        self.password_entry.pack(pady=5, ipady=3)
        
        btn = tk.Button(card, text="Log In" if has_account else "Register", font=("Arial", 10, "bold"), bg=COLOR_GREEN, fg=COLOR_BG, command=self.handle_login if has_account else self.handle_signup)
        btn.pack(pady=20, ipady=4)

    def animate_progress_bar(self, target_percentage: int, label_text: str, fill_color: str):
        def step_fill(current_pct):
            if current_pct > target_percentage:
                if target_percentage == 100:
                    self.bar_lbl.config(text="🎉 Action Finalized", fg=COLOR_GREEN)
                    import winsound
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
        self.bar_lbl.config(text="Ecosystem Idle", fg="#95a5a6")

    def toggle_sidebar(self):
        if self.sidebar_open: self.animate_sidebar(-self.sidebar_width, False)
        else: self.animate_sidebar(0, True)

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
        widget.bind("<Enter>", lambda e: widget.config(bg=color_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=color_base))

    def log_message(self, text):
        if not hasattr(self, 'log_box'): return
        formatted = f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n"
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, formatted)
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)

    def get_validated_uid(self):
        uid_str = self.uid_entry.get().strip()
        if not uid_str.isdigit(): return None
        return int(uid_str)

    def trigger_assign(self):
        uid = self.get_validated_uid()
        if not uid: return
        selected_rank = self.rank_combo.get()
        self.animate_progress_bar(100, "Node processing mutation", COLOR_GREEN)
        self.log_message(f"⌛ Relaying payload: User {uid} -> {selected_rank}")
        self.dispatch_to_node_api(uid, "assign", RANKS[selected_rank])

    def trigger_unassign(self):
        uid = self.get_validated_uid()
        if not uid: return
        self.animate_progress_bar(100, "Node processing reset", COLOR_RED)
        self.log_message(f"⌛ Relaying payload: Resetting User {uid}")
        self.dispatch_to_node_api(uid, "unassign", ROLE_DEFAULT_MEMBER)

    def dispatch_to_node_api(self, user_id, action, role_id):
        def network_send():
            import urllib.request
            payload = {"user_id": user_id, "action": action, "role_id": role_id}
            req = urllib.request.Request(
                "http://127.0.0",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "X-API-Key": "my66CQTQxNWWk12dQp3sbRSxBmRfLqBKUNUJ_5SPw_Y"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req) as res:
                    self.after(0, lambda: self.log_message(f"🎉 JS API Confirmation received."))
                self.run_java_companion(user_id, action, role_id)
            except Exception:
                self.after(0, lambda: self.log_message(f"❌ API Handshake Failed."))
        threading.Thread(target=network_send, daemon=True).start()

    def run_java_companion(self, user_id, action, rank_id):
        if not os.path.exists(JAVA_JAR_FILE): return
        def run():
            try:
                subprocess.run(["java", "-jar", JAVA_JAR_FILE, str(user_id), str(action), str(rank_id)], capture_output=True, text=True, check=True)
                self.after(0, lambda: self.log_message(f"☕ [Java Companion Ledger Logged]"))
            except Exception: pass
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    app = AnimatedBotApp()
    app.mainloop()
