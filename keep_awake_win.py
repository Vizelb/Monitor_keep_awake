#!/usr/bin/env python3
import ctypes
import time
import argparse

# Флаги Windows API
ES_CONTINUOUS       = 0x80000000
ES_SYSTEM_REQUIRED  = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def set_state(flags):
    if ctypes.windll.kernel32.SetThreadExecutionState(flags) == 0:
        raise ctypes.WinError()

def keep_awake(seconds=None, refresh=30, display_only=False):
    # По умолчанию блокируем и сон системы, и гашение дисплея
    flags = ES_CONTINUOUS | ES_DISPLAY_REQUIRED
    if not display_only:
        flags |= ES_SYSTEM_REQUIRED

    set_state(flags)
    try:
        deadline = None if seconds is None else time.monotonic() + seconds
        print("Windows: удерживаю экран включённым. Нажмите Ctrl+C для выхода.")
        while True:
            time.sleep( max(1, min(refresh, (deadline - time.monotonic()) if deadline else refresh)) )
            set_state(flags)  # периодически обновляем состояние
            if deadline is not None and time.monotonic() >= deadline:
                break
    finally:
        set_state(ES_CONTINUOUS)  # снимаем удержание
        print("Windows: удержание снято.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Не даёт Windows гасить монитор/уходить в сон по неактивности.")
    parser.add_argument("--minutes", type=float, help="Сколько минут держать экран включённым. По умолчанию — пока программа запущена.")
    parser.add_argument("--display-only", action="store_true", help="Только не давать гаснуть дисплею (сон системы не блокируется).")
    parser.add_argument("--refresh", type=int, default=30, help="Период обновления флага, сек (по умолчанию 30).")
    args = parser.parse_args()

    seconds = int(args.minutes * 60) if args.minutes else None
    keep_awake(seconds=seconds, refresh=args.refresh, display_only=args.display_only)