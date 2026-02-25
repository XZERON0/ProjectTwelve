# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_all, copy_metadata
# Собираем все подмодули для Django
django_hidden = collect_submodules('django')
tailwind_hidden = collect_submodules('tailwind')
theme_collection = collect_all('theme')

a = Analysis(
    ['run.py'],
    pathex=['.'],
    datas=[
        ('static', 'static'),
        ('app/templates', 'app/templates'),
        ('theme', 'theme'),
        ('db.sqlite3', '.'),
    ] + collect_data_files('tailwind') + theme_collection[0] + copy_metadata('django-auditlog'),
    binaries=[] + theme_collection[1],
    hiddenimports=[
        'django',
        'tailwind',
        'theme',
        'decouple',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'whitenoise',  
        'whitenoise.middleware',  
        'whitenoise.storage',  
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'tailwind.templatetags',
        'tailwind.utils',
        'tailwind.apps',
    ] + django_hidden + tailwind_hidden + theme_collection[2],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    noarchive=False
)

pyz = PYZ(a.pure)

exe = COLLECT(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)