# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
#             添加lupa模块
             binaries=[ ('venv/lib/python3.9/site-packages/lupa', 'lupa')],
             datas=[("toolsDir", "toolsDir"), ("res", "res"), ("toolsFramerwork", "toolsFramerwork")],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='res/131.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='猫咪工具箱')
app = BUNDLE(coll,
             name='猫咪工具箱.app',
             icon='res/131.ico',
             bundle_identifier=None)
