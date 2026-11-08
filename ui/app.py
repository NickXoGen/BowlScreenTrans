# ui/app.py
import tkinter as tk
from tkinter import ttk
import pystray
import pystray._win32
from PIL import Image, ImageDraw
import keyboard
import os
from config import HOTKEY
from ui.popup import PICTURES_DIR # Импортируем путь из popup

class App(tk.Tk):
    def __init__(self, snip_callback):
        super().__init__()
        self.snip_callback = snip_callback
        
        self.title("BowlScreenTrans")
        self.geometry("550x450") # Чуть увеличили окно
        self.resizable(False, False)
        self.configure(bg="#2b2b2b")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#2b2b2b", foreground="#d4d4d4", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#4ec9b0")
        style.configure("TButton", font=("Segoe UI", 10))
        
        header = ttk.Label(self, text="🚀 BowlScreenTrans", style="Header.TLabel")
        header.pack(pady=(15, 5))
        
        info_text = f"Хоткей: {HOTKEY.upper()} | Свернуть в трей: крестик"
        ttk.Label(self, text=info_text, foreground="#888888").pack(pady=(0, 10))
        
        # Рамка для кнопок
        btn_frame = tk.Frame(self, bg="#2b2b2b")
        btn_frame.pack(pady=5)
        
        self.btn_snip = ttk.Button(btn_frame, text="Выделить область", command=self.start_snip)
        self.btn_snip.pack(side="left", padx=5, ipadx=10, ipady=5)
        
        self.btn_folder = ttk.Button(btn_frame, text="📁 Скриншоты", command=self.open_screenshots_folder)
        self.btn_folder.pack(side="left", padx=5, ipadx=10, ipady=5)
        
        ttk.Label(self, text="Журнал переводов:", foreground="#a0a0a0").pack(anchor="w", padx=20, pady=(10, 0))
        
        log_frame = tk.Frame(self, bg="#1e1e1e")
        log_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
        self.journal = tk.Text(log_frame, bg="#1e1e1e", fg="#4ec9b0", font=("Consolas", 10), 
                               relief="flat", state="disabled", wrap="word")
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.journal.yview)
        self.journal.configure(yscrollcommand=scrollbar.set)
        
        self.journal.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tray_icon = None
        self.setup_tray()
        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

    def open_screenshots_folder(self):
        # Создаем папку, если ее нет, и открываем
        os.makedirs(PICTURES_DIR, exist_ok=True)
        os.startfile(PICTURES_DIR)

    def start_snip(self):
        self.snip_callback(self)

    def update_journal(self, text):
        self.journal.configure(state="normal")
        self.journal.delete(1.0, tk.END)
        self.journal.insert(tk.END, text)
        self.journal.configure(state="disabled")

    def clear_journal(self):
        self.journal.configure(state="normal")
        self.journal.delete(1.0, tk.END)
        self.journal.configure(state="disabled")
        self.deiconify()

    def setup_tray(self):
        image = Image.new('RGB', (64, 64), color=(43, 43, 43))
        d = ImageDraw.Draw(image)
        d.text((15, 15), "T", fill=(78, 201, 176))
        
        menu = pystray.Menu(
            pystray.MenuItem("Открыть", self.show_window, default=True),
            pystray.MenuItem("Выход", self.quit_app)
        )
        self.tray_icon = pystray.Icon("BowlScreenTrans", image, "BowlScreenTrans", menu)

    def hide_to_tray(self):
        self.withdraw()
        if not self.tray_icon.visible:
            self.tray_icon.run_detached()

    def show_window(self, icon=None, item=None):
        self.after(0, self.deiconify)

    def quit_app(self, icon=None, item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        try:
            keyboard.remove_hotkey(HOTKEY)
        except:
            pass
        self.after(0, self.destroy)