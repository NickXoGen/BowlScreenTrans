# main.py
from ui.app import App
from core.capture import SnippingTool
from ui.popup import TranslationOverlay
from core.translator import init_translator, process_image
from config import HOTKEY
import keyboard
import queue
import pystray
import pystray._win32

task_queue = queue.Queue()

def on_capture(app, img, x, y, width, height):
    """Вызывается после выделения области."""
    result_lines = process_image(img)
    
    if not result_lines:
        app.clear_journal()
        app.deiconify() # Показываем окно, если ничего не распознали
        return
        
    # Склеиваем текст для журнала
    journal_text = "\n".join([line['text'] for line in result_lines])
    
    # 1. Обновляем журнал
    app.update_journal(journal_text)
    
    # 2. ВОЗВРАЩАЕМ ОКНО (чтобы ты видел журнал)
    app.deiconify() 
    
    # 3. Показываем оверлей
    TranslationOverlay(app, img, result_lines, x, y, width, height, on_close_cb=app.clear_journal)

def start_snip(app):
    # Прячем окно, чтобы оно не попало в скриншот
    app.withdraw()
    
    def callback(img, x, y, w, h):
        on_capture(app, img, x, y, w, h)
    SnippingTool(app, callback)

def check_queue(app):
    try:
        while True:
            task = task_queue.get_nowait()
            if task == "snip":
                start_snip(app)
    except queue.Empty:
        pass
    app.after(100, lambda: check_queue(app))

def main():
    init_translator()
    
    def trigger_snip(app_instance):
        start_snip(app_instance)

    app = App(snip_callback=trigger_snip)
    keyboard.add_hotkey(HOTKEY, lambda: task_queue.put("snip"))
    check_queue(app)
    
    print(f"Программа запущена. Хоткей: {HOTKEY.upper()}")
    app.mainloop()

if __name__ == "__main__":
    main()