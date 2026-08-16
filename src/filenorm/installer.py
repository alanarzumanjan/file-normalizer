import ctypes
import os
import shutil
import sys
import winreg


def install_for_windows():
    """Install filenorm to the user's local application directory."""
    if sys.platform != "win32":
        print("This feature is only available for Windows.")
        return

    install_dir = os.path.expandvars(r"%LOCALAPPDATA%\Filenorm")
    os.makedirs(install_dir, exist_ok=True)

    current_exe = sys.executable

    if not current_exe.lower().endswith(".exe"):
        print("This command must be run from the compiled filenorm executable.")
        return

    target_exe = os.path.join(install_dir, "filenorm.exe")

    try:
        shutil.copy2(current_exe, target_exe)
        print(f"File successfully copied to: {target_exe}")
    except OSError as error:
        print(f"Error while copying file: {error}")
        return

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE,
        ) as key:
            try:
                path_value, _ = winreg.QueryValueEx(key, "PATH")
            except FileNotFoundError:
                path_value = ""

            if install_dir.lower() in path_value.lower():
                print("Path is already present in environment variables.")
                return

            new_path = (
                f"{path_value};{install_dir}"
                if path_value
                else install_dir
            )

            winreg.SetValueEx(
                key,
                "PATH",
                0,
                winreg.REG_EXPAND_SZ,
                new_path,
            )

    except OSError as error:
        print(f"Failed to update registry: {error}")
        return

    notify_environment_change()

    print("Success! Utility added to environment variables.")
    print(
        "Restart your terminal (PowerShell/CMD) "
        "for the 'filenorm' command to work globally."
    )


def notify_environment_change():
    """Notify Windows applications that the environment has changed."""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002

    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Environment",
        SMTO_ABORTIFHUNG,
        5000,
        None,
    )