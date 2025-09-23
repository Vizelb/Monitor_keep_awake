# Запуск скрипта

    1. Переходим в нужный файл
    2. ctrl+shift+b -> enter (то что выпадет - "▶ start current .py script")

# Как пользоваться

## keep_awake.py

- Бессрочно (пока скрипт запущен): python keep_awake.py
- На N минут: python keep_awake.py --minutes 120

## keep_awake_win.py

- Бессрочно: python keep_awake_win.py
- На 2 часа: python keep_awake_win.py --minutes 120
- Только не гасить дисплей (не блокируя общий сон системы): python keep_awake_win.py --display-only

## dist/keep_awake_win.exe

- тоже самое, что и "keep_awake_win.py" - только в расширении .exe

# Tasks.json

```
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "▶ start current .py script",
      "type": "shell",
      // Используем переменную, которая автоматически подставляет путь 
      // к выбранному Python-интерпретатору
      // "command": "${command:python.interpreterPath}", 
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": [
        "${file}"
      ],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

# Start script

```
Чтобы запустить скрипт на Python на ПК, тебе нужно

---

1. Установить сам Python

- Скачай Python с официального сайта  
  [httpswww.python.orgdownloads](httpswww.python.orgdownloads)
- Выбери версию (обычно рекомендуется последняя стабильная, например, Python 3.12.x).
- При установке обязательно поставь галочку “Add Python to PATH” (это упростит запуск из командной строки).

---

2. (Опционально) Установить нужные библиотеки

- Если твой скрипт использует сторонние библиотеки (например, `numpy`, `requests`, `pandas` и т.д.), их нужно установить через pip
  pip install имя_библиотеки
  
- Если есть файл `requirements.txt`, то
  pip install -r requirements.txt
  

---

3. Запустить скрипт

- Открой командную строку (cmd, PowerShell или терминал).
- Перейди в папку со скриптом
  cd путь_к_папке
  
- Запусти скрипт
  python имя_файла.py
  
  или, если у тебя несколько версий Python
  python3 имя_файла.py
  

---

4. (Опционально) Установить редактор кода

- Для удобства можешь установить редактор, например
  - [VS Code](httpscode.visualstudio.com)
  - [PyCharm](httpswww.jetbrains.compycharm)
  - [Sublime Text](httpswww.sublimetext.com)

```

# TODO
