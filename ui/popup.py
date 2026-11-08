# ui/popup.py
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import datetime

# Находим папку Pictures текущего пользователя
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "BowlScreenTrans")

class TranslationOverlay(tk.Toplevel):
    def __init__(self, master, img_pil, translated_lines, x, y, width, height, on_close_cb):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.on_close_cb = on_close_cb
        
        img_rgba = img_pil.convert("RGBA")
        draw = ImageDraw.Draw(img_rgba)
        
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
        except:
            font = ImageFont.load_default()

        for line in translated_lines:
            text = line['text']
            left, top, right, bottom = line['rect']
            draw.rectangle([left-2, top-2, right+2, bottom+2], fill=(30, 30, 35))
            draw.text((left, top), text, font=font, fill=(78, 201, 176))

        self.save_screenshot(img_rgba)

        self.photo = ImageTk.PhotoImage(img_rgba)
        self.label = tk.Label(self, image=self.photo, bg="#141414")
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.label.bind("<Button-1>", self.close)
        self.bind("<Escape>", self.close)
        self.focus_force()

    def save_screenshot(self, img):
        os.makedirs(PICTURES_DIR, exist_ok=True)
        
        files = [os.path.join(PICTURES_DIR, f) for f in os.listdir(PICTURES_DIR) if f.endswith(".png")]
        if len(files) >= 50:
            oldest_file = min(files, key=os.path.getctime)
            try:
                os.remove(oldest_file)
            except Exception as e:
                print(f"Не удалось удалить старый скрин: {e}")

        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f.png")
        filepath = os.path.join(PICTURES_DIR, filename)
        img.save(filepath)

    def close(self, event=None):
        if self.on_close_cb:
            self.on_close_cb()
        self.destroy()