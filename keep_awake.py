#!/usr/bin/env python3
import sys
import time
import argparse
import subprocess
import shutil
import re

def keep_awake_windows(seconds=None):
    import ctypes
    kernel32 = ctypes.windll.kernel32
    ES_CONTINUOUS       = 0x80000000
    ES_SYSTEM_REQUIRED  = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002

    def set_state(flags):
        if kernel32.SetThreadExecutionState(flags) == 0:
            raise ctypes.WinError()

    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    set_state(flags)
    try:
        deadline = None if seconds is None else time.monotonic() + seconds
        print("Windows: удерживаю экран включённым. Нажмите Ctrl+C для выхода.")
        while True:
            time.sleep(30)
            set_state(flags)  # обновляем состояние периодически
            if deadline is not None and time.monotonic() >= deadline:
                break
    finally:
        set_state(ES_CONTINUOUS)  # снимаем удержание
        print("Windows: удержание снято.")

def keep_awake_macos(seconds=None):
    # caffeinate встроен в macOS. -d не даёт гаснуть дисплею, -i блокирует idle sleep
    if seconds is None:
        proc = subprocess.Popen(["caffeinate", "-di"])
        print("macOS: запущен caffeinate. Нажмите Ctrl+C для выхода.")
        try:
            proc.wait()
        except KeyboardInterrupt:
            pass
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except Exception:
                proc.kill()
            print("macOS: удержание снято.")
    else:
        print(f"macOS: удерживаю экран ~{seconds} сек.")
        subprocess.call(["caffeinate", "-di", "-t", str(int(seconds))])
        print("macOS: удержание снято.")

def keep_awake_linux(seconds=None):
    import time
    # 1) Пытаемся через freedesktop DBus (gdbus)
    if shutil.which("gdbus"):
        try:
            out = subprocess.check_output([
                "gdbus", "call", "--session",
                "--dest", "org.freedesktop.ScreenSaver",
                "--object-path", "/org/freedesktop/ScreenSaver",
                "--method", "org.freedesktop.ScreenSaver.Inhibit",
                "keep_awake.py", "Prevent idle"
            ], text=True).strip()
            m = re.search(r'uint32\s+(\d+)', out)
            cookie = m.group(1) if m else None
            if cookie:
                print("Linux(DBus): удерживаю экран. Нажмите Ctrl+C для выхода.")
                try:
                    if seconds is None:
                        while True:
                            time.sleep(3600)
                    else:
                        time.sleep(seconds)
                finally:
                    subprocess.call([
                        "gdbus", "call", "--session",
                        "--dest", "org.freedesktop.ScreenSaver",
                        "--object-path", "/org/freedesktop/ScreenSaver",
                        "--method", "org.freedesktop.ScreenSaver.UnInhibit",
                        cookie
                    ])
                    print("Linux(DBus): удержание снято.")
                return
        except Exception:
            pass

    # 2) Фолбек: периодически «пингуем» xdg-screensaver
    if shutil.which("xdg-screensaver"):
        print("Linux(xdg-screensaver): удерживаю экран. Нажмите Ctrl+C для выхода.")
        deadline = None if seconds is None else time.monotonic() + seconds
        try:
            while True:
                subprocess.call(["xdg-screensaver", "reset"])
                time.sleep(50)
                if deadline is not None and time.monotonic() >= deadline:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            print("Linux(xdg-screensaver): удержание снято.")
        return

    # 3) Ещё один фолбек: xdotool (лёгкое «шевеление» мышью)
    if shutil.which("xdotool"):
        print("Linux(xdotool): удерживаю экран. Нажмите Ctrl+C для выхода.")
        deadline = None if seconds is None else time.monotonic() + seconds
        try:
            while True:
                subprocess.call(["xdotool", "mousemove_relative", "--", "1", "0"])
                subprocess.call(["xdotool", "mousemove_relative", "--", "-1", "0"])
                time.sleep(59)
                if deadline is not None and time.monotonic() >= deadline:
                    break
        except KeyboardInterrupt:
            pass
        finally:
            print("Linux(xdotool): удержание снято.")
        return

    print("Не найдено подходящего способа (gdbus/xdg-screensaver/xdotool). "
          "Установите один из них, например: sudo apt install libglib2.0-bin xdg-utils")

def main():
    parser = argparse.ArgumentParser(description="Не даёт монитору погаснуть при неактивности.")
    parser.add_argument("--minutes", type=float, default=None,
                        help="Сколько минут держать экран включённым. По умолчанию — пока программа запущена.")
    args = parser.parse_args()
    seconds = None if args.minutes is None else int(args.minutes * 60)

    if sys.platform.startswith("win"):
        keep_awake_windows(seconds)
    elif sys.platform == "darwin":
        keep_awake_macos(seconds)
    else:
        keep_awake_linux(seconds)

if __name__ == "__main__":
    main()