import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "main.py",
        "--name",
        "PyGarden",
        "--icon",
        "assets/icon.png",
        "--onefile",
        "--windowed",
        "--add-data",
        "assets:assets",
        "--clean",
    ]
)
