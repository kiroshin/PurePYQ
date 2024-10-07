# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['Pure/main.py'],
    pathex=[],
    binaries=[],
    datas=[('Pure/assets', 'assets')],
    hiddenimports=[],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pure',                        # 윈도우용 이름
    icon='Pure/assets/appicon.ico',     # 윈도우용 아이콘
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
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='pure',                        # 패키지 파일
)
app = BUNDLE(
    coll,
    name='Pure.app',                    # 맥용 이름
    icon='Pure/assets/appicon.icns',    # 맥용 아이콘
    bundle_identifier=None,
)
