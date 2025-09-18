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

# TODO:
    
    