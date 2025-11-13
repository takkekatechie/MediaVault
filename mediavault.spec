# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for MediaVault Scanner
This file defines how to build the Windows executable.

Usage:
    pyinstaller mediavault.spec

The resulting executable will be in the 'dist' folder.
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all necessary data files
datas = []

# Add OpenCV Haar Cascade files
import cv2
cv2_data_path = os.path.dirname(cv2.__file__)
haar_cascade_path = os.path.join(cv2_data_path, 'data', 'haarcascade_frontalface_default.xml')
if os.path.exists(haar_cascade_path):
    datas.append((haar_cascade_path, 'cv2/data'))

# Collect CustomTkinter assets
try:
    ctk_datas = collect_data_files('customtkinter')
    datas.extend(ctk_datas)
except:
    pass

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PIL._tkinter_finder',
    'customtkinter',
    'pytesseract',
    'exifread',
    'cv2',
    'numpy',
    'sqlite3',
]

# Collect all submodules
hiddenimports.extend(collect_submodules('customtkinter'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'pytest',
        'setuptools',
    ],
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
    name='MediaVaultScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for windowed app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one: icon='icon.ico'
)

# Note: To add an icon, create or download an .ico file and set:
# icon='path/to/icon.ico'

