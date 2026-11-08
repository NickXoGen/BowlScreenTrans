# build.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5) # <--- ВОТ ЭТА СТРОЧКА ЛЕЧИТ ОШИБКУ

from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []

packages_to_collect = [
    'argostranslate', 'stanza', 'torch', 'spacy', 
    'pytesseract', 'pystray', 'PIL', 'sentencepiece'
]

for pkg in packages_to_collect:
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

hiddenimports += ['keyboard', 'mss', 'pystray._win32']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorboard'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BowlScreenTrans',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)