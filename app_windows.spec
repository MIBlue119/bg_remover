# -*- mode: python -*-
import os 
import platform 


from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
block_cipher = None
bundle_id = "com.unlimiter.bg_remover"
excludes = []
excluded_binaries = []
pathex = []

a = Analysis(['app.py'],
             pathex=pathex,
             binaries=[]+collect_dynamic_libs("rembg"),
             datas= []+collect_data_files('rembg', include_py_files=True, subdir=None, excludes=None, includes=None),
             hiddenimports=['icecream'],
             hookspath=["installer/pyinstaller-hooks"], 
             runtime_hooks=[],
             excludes=excludes,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='bg_remover',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='installer/resources/images/bg_remover.ico' 
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='bg_remover')

