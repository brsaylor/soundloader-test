# -*- mode: python -*-

import glob
import os.path
import re
import subprocess
from PyInstaller.depend import bindepend

block_cipher = None
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks


GST_PLUGINS_DIR = 'gst-plugins'


def find_gst_plugin_path():
    p = subprocess.Popen(
        ['gst-inspect-1.0', 'coreelements'],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    (stdoutdata, stderrdata) = p.communicate()

    match = re.search(r'^\s*Filename\s+(\S+)', stdoutdata, re.MULTILINE)

    if not match:
        return None

    return os.path.dirname(match.group(1))


def get_gst_plugin_binaries():
    plugin_path = find_gst_plugin_path()

    binaries = []
    for pattern in ['libgst*.dll', 'libgst*.dylib', 'libgst*.so']:
        pattern = os.path.join(plugin_path, pattern)
        binaries += [(f, GST_PLUGINS_DIR) for f in glob.glob(pattern)]

    return binaries

def get_gst_binaries():
    plugin_binaries = get_gst_plugin_binaries()

    lib_paths = set()
    for plugin_filepath, _ in plugin_binaries:
        plugin_deps = bindepend.selectImports(plugin_filepath)
        lib_paths.update([lib_path for _, lib_path in plugin_deps])

    lib_binaries = [(f, '.') for f in lib_paths]

    return plugin_binaries + lib_binaries

a = Analysis(['../testapp/main.py'],
             pathex=['.'],
             binaries=get_gst_binaries(),
             datas=[],
             #hiddenimports=[],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             #excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,
             **get_deps_all())
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
