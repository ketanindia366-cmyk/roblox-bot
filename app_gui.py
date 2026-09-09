# Save as app_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import winsound

COLOR_BG = "#1e1e2e"       
COLOR_PANEL = "#252538"    
COLOR_TEXT = "#cdd6f4"     
COLOR_ACCENT = "#cba6f7"   
COLOR_GREEN = "#a6e3a1"    
COLOR_RED = "#f38ba8"      

class AppGUI:
    def __init__(self, app):
        self.app = app

    def build_main_dashboard(self):
        self.app.top_bar = tk.Frame(self.app, bg=COLOR_PANEL, height=50)
        self.app.top_bar.pack(fill=tk.X)
        self.app.top_bar.pack_propagate(False)
        
        self.app.menu_btn = tk.Button(self.app.top_bar, text="📋 App Logs", font=("Arial", 11, "bold"), bg=COLOR_PANEL, fg=COLOR_ACCENT, bd=0, activebackground=COLOR_BG, activeforeground=COLOR_TEXT, command=self.app.toggle_sidebar)
        self.app.menu_btn.pack(side=tk.LEFT, padx=15)
        
        title_lbl = tk.Label(self.app.top_bar, text="UNIFIED NODE & PYTHON GATEWAY", font=("Arial", 11, "bold"), fg=COLOR_TEXT, bg=COLOR_PANEL)
        title_lbl.pack(side=tk.LEFT, padx=10)
        
        self.app.main_container = tk.Frame(self.app, bg=COLOR_BG)
        self.app.main_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.app.logo_canvas = tk.Canvas(self.app.main_container, width=80, height=80, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.app.logo_canvas.pack(pady=(5, 5))
        self.app.logo_canvas.create_polygon(40, 5, 75, 20, 75, 55, 40, 75, 5, 55, 5, 20, fill=COLOR_PANEL, outline=COLOR_ACCENT, width=2)
        self.app.logo_canvas.create_text(40, 40, text="🌐", font=("Arial", 22), fill=COLOR_TEXT)
        
        self.app.card = tk.Frame(self.app.main_container, bg=COLOR_PANEL, width=420, height=330, highlightbackground="#313244", highlightthickness=1)
        self.app.card.pack(pady=5)
        self.app.card.pack_propagate(False)
        
        uid_lbl = tk.Label(self.app.card, text="Target Player User ID", font=("Arial", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        uid_lbl.pack(pady=(15, 3), anchor="w", padx=40)
        
        self.app.uid_entry = tk.Entry(self.app.card, font=("Arial", 12), width=34, bg=COLOR_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, bd=0, highlightthickness=1, highlightbackground="#313244", highlightcolor=COLOR_ACCENT)
        self.app.uid_entry.pack(pady=2, ipady=4)
        
        rank_lbl = tk.Label(self.app.card, text="Destination Group Rank", font=("Arial", 10, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        rank_lbl.pack(pady=(10, 3), anchor="w", padx=40)
        
        self.app.rank_combo = ttk.Combobox(self.app.card, values=list(self.app.ranks.keys()), state="readonly", width=36, font=("Arial", 11))
        self.app.rank_combo.set(list(self.app.ranks.keys()))
        self.app.rank_combo.pack(pady=2)
        
        self.app.bar_lbl = tk.Label(self.app.card, text="Ecosystem Idle", font=("Arial", 9, "bold"), fg="#95a5a6", bg=COLOR_PANEL)
        self.app.bar_lbl.pack(pady=(15, 2), anchor="w", padx=40)
        
        self.app.bar_canvas = tk.Canvas(self.app.card, width=340, height=14, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.app.bar_canvas.pack(pady=2)
        self.app.bar_canvas.create_rectangle(0, 0, 340, 14, fill="#181825", width=0, tags="track")
        
        btn_frame = tk.Frame(self.app.card, bg=COLOR_PANEL)
        btn_frame.pack(pady=20, fill=tk.X, padx=40)
        
        self.app.assign_btn = tk.Button(btn_frame, text="Assign Rank", font=("Arial", 10, "bold"), bg=COLOR_GREEN, fg=COLOR_BG, bd=0, cursor="hand2", width=14, command=self.app.trigger_assign)
        self.app.assign_btn.pack(side=tk.LEFT, ipady=6)
        self.app.setup_hover_effect(self.app.assign_btn, COLOR_GREEN, "#b4befe")
        
        self.app.reset_btn = tk.Button(btn_frame, text="Reset Member", font=("Arial", 10, "bold"), bg=COLOR_RED, fg=COLOR_BG, bd=0, cursor="hand2", width=14, command=self.app.trigger_unassign)
        self.app.reset_btn.pack(side=tk.RIGHT, ipady=6)
        self.app.setup_hover_effect(self.app.reset_btn, COLOR_RED, "#f5e0dc")
        
        self.app.sidebar = tk.Frame(self.app, bg=COLOR_PANEL, width=0, highlightbackground="#313244", highlightthickness=1)
        self.app.sidebar.place(x=-self.app.sidebar_width, y=50, height=510)
        self.app.sidebar.pack_propagate(False)
        
        side_title = tk.Label(self.app.sidebar, text="Ecosystem Terminal", font=("Arial", 11, "bold"), fg=COLOR_ACCENT, bg=COLOR_PANEL)
        side_title.pack(pady=10, anchor="w", padx=15)
        
        self.app.log_box = tk.Text(self.app.sidebar, bg=COLOR_BG, fg=COLOR_TEXT, font=("Courier", 9), state=tk.DISABLED, bd=0, wrap=tk.WORD)
        self.app.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
