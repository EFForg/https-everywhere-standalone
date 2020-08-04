# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['https-everywhere-mitmproxy.py'],
             pathex=['/home/user/workspace/https-everywhere-mitmproxy'],
             binaries=[],
             datas=[('update_channels.json', '.'), ('web_ui/templates', 'web_ui/templates'), ('web_ui/static', 'web_ui/static')],
             hiddenimports=['configparser'],
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
          name='https-everywhere-mitmproxy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
