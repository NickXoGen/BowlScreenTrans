# core/translator.py
import argostranslate.package
import argostranslate.translate
import pytesseract
from pytesseract import Output
from PIL import Image
import re
from config import TESSERACT_CMD

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def init_translator():
    print("Проверка базовых языковых пакетов...")
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    installed_packages = argostranslate.package.get_installed_packages()
    for from_code, to_code in [("en", "ru"), ("ru", "en")]:
        if not any(p.from_code == from_code and p.to_code == to_code for p in installed_packages):
            package = next((x for x in available_packages if x.from_code == from_code and x.to_code == to_code), None)
            if package:
                argostranslate.package.install_from_path(package.download())

def process_image(image: Image.Image):
    """Возвращает список строк с координатами и переводом."""
    try:
        # Получаем данные о каждой строчке
        d = pytesseract.image_to_data(image, lang='eng+rus', output_type=Output.DICT)
        
        lines = {}
        n_boxes = len(d['level'])
        
        # Группируем слова в строки по их координатам
        for i in range(n_boxes):
            if int(d['conf'][i]) > 40: # Отсеиваем мусор (уверенность ниже 40%)
                block, par, line = d['block_num'][i], d['par_num'][i], d['line_num'][i]
                key = (block, par, line)
                
                if key not in lines:
                    lines[key] = {
                        'text': '',
                        'left': d['left'][i], 'top': d['top'][i],
                        'right': d['left'][i] + d['width'][i],
                        'bottom': d['top'][i] + d['height'][i]
                    }
                else:
                    lines[key]['right'] = max(lines[key]['right'], d['left'][i] + d['width'][i])
                    lines[key]['bottom'] = max(lines[key]['bottom'], d['top'][i] + d['height'][i])
                
                lines[key]['text'] += d['text'][i] + " "

        result = []
        for key, line in lines.items():
            text = line['text'].strip()
            if not text: continue
            
            has_cyrillic = bool(re.search('[а-яА-ЯёЁ]', text))
            src_lang, dest_lang = ("ru", "en") if has_cyrillic else ("en", "ru")
            
            try:
                translated = argostranslate.translate.translate(text, src_lang, dest_lang)
            except:
                translated = text # Если перевод не удался, оставляем как есть

            result.append({
                'text': translated,
                'rect': (line['left'], line['top'], line['right'], line['bottom'])
            })
            
        return result
    except Exception as e:
        print(f"Ошибка OCR: {e}")
        return []