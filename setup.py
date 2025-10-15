import sys
from cx_Freeze import setup, Executable

# Указываем, что это приложение с графическим интерфейсом для Windows
# "Win32GUI" убирает черное окно консоли при запуске .exe
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Определяем исполняемый файл
# 'file_organizer.py' - это имя вашего главного скрипта
executables = [Executable("file_organizer.py", base=base, target_name="FileOrganizer.exe")]

# Настройки сборки
# В 'packages' можно добавить библиотеки, которые cx_Freeze мог пропустить
# В 'include_files' можно добавить доп. файлы (иконки, картинки, конфиги)
build_exe_options = {
    "packages": ["os", "tkinter", "customtkinter", "shutil", "subprocess"],
    "include_files": [], # Если бы у вас была иконка, добавили бы сюда: ["icon.ico"]
}

# Основная функция setup
setup(
    name="FileOrganizer",
    version="1.0",
    description="Удобный органайзер для рабочих файлов",
    options={"build_exe": build_exe_options},
    executables=executables,
)