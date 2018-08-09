from cx_Freeze import setup, Executable

base = None
executables = [Executable("crawler_main.py", base = base)]

packages = [
    "time",
    "logging",
    "csv",
    "selenium",
    "urllib",
    "collections",
    "bs4",
    "lxml"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "<shimo crawler>",
    options = options,
    version = "0.1",
    description = '<Crawler for shimo documents>',
    executables = executables
)
