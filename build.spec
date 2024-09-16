# -*- mode: python ; coding: utf-8 -*-

extra_files = [
    ('assets/template_matching/*', 'assets/template_matching/'),
    ('assets/issue/*', 'assets/issue/'),
    ('pyproject.toml', '.')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=extra_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NexusDownloadFlow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
