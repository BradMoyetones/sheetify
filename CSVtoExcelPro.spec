# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')], 
    hiddenimports=[
        'pandas', 'xlsxwriter', 'openpyxl', 'PySide6.QtSvg', 'PySide6.QtCore',
        'PySide6.QtWidgets', 'PySide6.QtGui', 'numpy', 'numpy.core._methods', 
        'numpy.lib.format', 'secrets'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    strip=False,
    upx=False,
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None
)

app = BUNDLE(
    exe,
    name='CSV-to-Excel-Pro.app',
    icon=None,
    bundle_identifier='com.brad.csvtoexcel',
)