# -*- mode: python -*-

block_cipher = None
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, get_deps_minimal, hookspath, runtime_hooks

kivy_deps = get_deps_minimal(video=None, window=True, audio=['gstplayer'])
# kivy_deps = get_deps_all()

a = Analysis(['../testapp/main.py'],
             pathex=['.'],
             datas=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **kivy_deps)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='soundloader-test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('../testapp/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='soundloader-test')
app = BUNDLE(coll,
             name='soundloader-test.app',
             icon=None,
             bundle_identifier=None)
