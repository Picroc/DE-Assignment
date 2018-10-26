from cx_Freeze import setup, Executable

includes = ['numpy.core._methods', 'numpy.lib.format', 'sys', 'pyqtgraph.debug', 'pyqtgraph.ThreadsafeTimer']

setup(
    name="21",
    version="0.1",
    description="Blackjack",
    options={'build_exe': {'includes': includes}},
    executables=[Executable("final.py")]
)
