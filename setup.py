import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

files = [
    (os.path.abspath(entry.path), entry.path) for entry in os.scandir('./assets')
]

buildOptions = dict(packages = ["pyglet", "toyblock"], excludes = [], include_files = files)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name='Fuel4TheLight',
      version = '1.0',
      description = "Climb up those stairs and don't get out of fuel!",
      options = dict(build_exe = buildOptions),
      executables = executables)
