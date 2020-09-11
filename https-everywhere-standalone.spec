# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

hiddenimports = ['configparser', 'pkg_resources.py2_warn']
if sys.platform == "win32":
             hiddenimports.append('pystray._win32')

a = Analysis(['https-everywhere-standalone.py'],
             pathex=['/home/user/workspace/https-everywhere-standalone'],
             binaries=[],
             datas=[('update_channels.json', '.'), ('icon.png', '.'), ('web_ui/templates', 'web_ui/templates'), ('web_ui/static', 'web_ui/static')],
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='https-everywhere-standalone',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
