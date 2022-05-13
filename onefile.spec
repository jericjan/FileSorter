# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=["C:\\Program Files\\VideoLAN\\VLC\\","C:\\Users\\USER\\Desktop\\JJ\\python\\file sorter\\venv\\Lib\\site-packages"],
    binaries=[("C:/Program Files/VideoLAN/VLC/plugins/*", "plugins")],
    datas=[],
    hiddenimports=['vlc'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
splash = Splash(
    'filesorter.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries + [("libVLC.dll", "C:/Program Files/VideoLAN/VLC/libvlc.dll", "BINARY")],
    a.zipfiles,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='FileSorter',
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
	icon="filesorter.ico"
)
