import sys
import os
import shutil
import ctypes
import winreg

# This function installs the filenorm utility for Windows by copying the current executable to a specific directory and adding that directory to the user's PATH environment variable.
def install_for_windows():
    if sys.platform != "win32":
        print("This feature is only available for Windows.")
        return

    install_dir = os.path.expandvars(r"%LOCALAPPDATA%\Filenorm")
    os.makedirs(install_dir, exist_ok=True)
    
    current_exe = sys.executable
    target_exe = os.path.join(install_dir, "filenorm.exe")

    try:
        shutil.copy2(current_exe, target_exe)
        print(f"File successfully copied to: {target_exe}")
    except Exception as e:
        print(f"Error while copying file: {e}")
        return

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        try:
            path_val, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            path_val = ""

        if install_dir.lower() not in path_val.lower():
            new_path = f"{path_val};{install_dir}" if path_val else install_dir
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            SMTO_ABORTIFHUNG = 0x0002
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, None
            )
            print("Success! Utility added to environment variables.")
            print("Restart your terminal (PowerShell/CMD) for the 'filenorm' command to work globally.")
        else:
            print("Path is already present in environment variables.")
    except Exception as e:
        print(f"Failed to update registry: {e}")
