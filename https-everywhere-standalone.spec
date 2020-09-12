# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

hiddenimports = ['configparser', 'pkg_resources.py2_warn']
datas = [('update_channels.json', '.'), ('web_ui/templates', 'web_ui/templates'), ('web_ui/static', 'web_ui/static')]
if sys.platform == "win32":
             hiddenimports.append('pystray._win32')
             datas.append(('icon.png', '.'))
             datas.append(('icon-disabled.png', '.'))
             datas.append(('icon-blocking.png', '.'))

a = Analysis(['https-everywhere-standalone.py'],
             pathex=['/home/user/workspace/https-everywhere-standalone'],
             binaries=[],
             datas=datas,
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
