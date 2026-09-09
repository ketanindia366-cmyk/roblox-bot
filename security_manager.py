# Save as security_manager.py
import json
import os
import subprocess
import hashlib
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox

from app_config import COLOR_BG, COLOR_PANEL, COLOR_TEXT, COLOR_ACCENT, COLOR_GREEN, AUTH_FILE, NODE_SERVER_FILE, HTML_DASHBOARD, JAVA_JAR_FILE

class SecurityManager:
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def build_auth_screen(self, parent_window, success_callback):
        self.success_callback = success_callback
        self.auth_frame = tk.Frame(parent_window, bg=COLOR_BG)
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
            login_btn = tk.Button(card, text="Authenticate Now", font=("Arial", 10, "bold"), bg=COLOR_GREEN, fg=COLOR_BG, bd=0, cursor="hand2", width=20, command=self.process_login)
            login_btn.pack(pady=20, ipady=4)
        else:
            signup_btn = tk.Button(card, text="Register Credentials", font=("Arial", 10, "bold"), bg=COLOR_ACCENT, fg=COLOR_BG, bd=0, cursor="hand2", width=20, command=self.process_signup)
            signup_btn.pack(pady=20, ipady=4)

    def process_signup(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not email or "@" not in email or not password:
            messagebox.showerror("Auth Failure", "Please enter a valid email structure.")
            return
        auth_payload = {"registered_email": email, "password_hash": self.hash_password(password)}
        with open(AUTH_FILE, "w") as f:
            json.dump(auth_payload, f, indent=4)
        messagebox.showinfo("Success", "Account created successfully.")
        
        # Fresh frame reset tracking layout
        parent = self.auth_frame.master
        self.auth_frame.destroy()
        self.build_auth_screen(parent, self.success_callback)

    def process_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        with open(AUTH_FILE, "r") as f:
            stored_data = json.load(f)
        if email == stored_data["registered_email"] and self.hash_password(password) == stored_data["password_hash"]:
            self.auth_frame.destroy()
            self.success_callback()
        else:
            messagebox.showerror("Auth Error", "Access Denied.")

    def start_node_backend(self):
        if not os.path.exists(NODE_SERVER_FILE): return
        def boot():
            try:
                subprocess.Popen(["node", NODE_SERVER_FILE], shell=True)
            except Exception:
                pass
        threading.Thread(target=boot, daemon=True).start()

    def open_web_dashboard(self):
        if os.path.exists(HTML_DASHBOARD):
            webbrowser.open(os.path.abspath(HTML_DASHBOARD))

    def dispatch_to_node_api(self, app_instance, user_id, action, role_id):
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
                    app_instance.after(0, lambda: app_instance.log_message(f"🎉 JS API Confirmation received successfully."))
                self.run_java_companion(app_instance, user_id, action, role_id)
            except Exception:
                app_instance.after(0, lambda: app_instance.log_message(f"❌ API Handshake Failed: Node server rejected package."))
        threading.Thread(target=network_send, daemon=True).start()

    def run_java_companion(self, app_instance, user_id, action, rank_id):
        if not os.path.exists(JAVA_JAR_FILE): return
        def run():
            try:
                cmd = ["java", "-jar", JAVA_JAR_FILE, str(user_id), str(action), str(rank_id)]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                app_instance.after(0, lambda: app_instance.log_message(f"☕ [Java Companion Ledger]: {res.stdout.strip()}"))
            except Exception:
                pass
        threading.Thread(target=run, daemon=True).start()
