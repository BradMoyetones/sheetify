# -*- mode: python ; coding: utf-8 -*-
import sys
import os

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')], 
    hiddenimports=['pandas', 'xlsxwriter', 'openpyxl', 'PySide6.QtSvg'],
    excludes=['tkinter', 'unittest', 'email'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CSV-to-Excel-Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True, # Limpia símbolos para que pese menos
    upx=True,   # Comprime el binario
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None
)

# En Mac seguimos necesitando el BUNDLE para el .app
app = BUNDLE(
    exe,
    name='CSV-to-Excel-Pro.app',
    icon=None,
    bundle_identifier='com.brad.csvtoexcel',
)