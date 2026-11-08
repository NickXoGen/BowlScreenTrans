# core/capture.py
import tkinter as tk
import mss
from PIL import Image

class SnippingTool(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.configure(cursor="cross", bg="black")
        
        self.canvas = tk.Canvas(self, cursor="cross", bg="grey11", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Escape>", lambda e: self.destroy())

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        width = x2 - x1
        height = y2 - y1
        
        if width > 5 and height > 5:
            with mss.mss() as sct:
                monitor = {"top": y1, "left": x1, "width": width, "height": height}
                img = sct.grab(monitor)
                img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                
                self.callback(img_pil, x1, y1, width, height)
                
        self.destroy()