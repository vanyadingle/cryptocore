"""
Модуль для работы с файлами.
Автор: Ivan
"""
import os
import sys


def прочитать_файл(путь: str) -> bytes:
    """
    Читает файл в бинарном режиме.
    
    Args:
        путь: путь к файлу
        
    Returns:
        содержимое файла как байты
        
    Raises:
        SystemExit: если файл не найден или ошибка чтения
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(путь):
            raise FileNotFoundError(f"Файл не найден: {путь}")
        
        # Читаем файл в бинарном режиме
        with open(путь, 'rb') as файл:
            содержимое = файл.read()
        
        return содержимое
        
    except FileNotFoundError as ошибка:
        print(f"Ошибка: {ошибка}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Ошибка: нет доступа к файлу {путь}", file=sys.stderr)
        sys.exit(1)
    except Exception as ошибка:
        print(f"Ошибка чтения файла {путь}: {ошибка}", file=sys.stderr)
        sys.exit(1)


def записать_файл(путь: str, данные: bytes) -> None:
    """
    Записывает данные в файл в бинарном режиме.
    
    Args:
        путь: путь к файлу
        данные: данные для записи
        
    Raises:
        SystemExit: если ошибка записи
    """
    try:
        # Создаем директорию, если она не существует
        директория = os.path.dirname(путь)
        if директория and not os.path.exists(директория):
            os.makedirs(директория)
        
        # Записываем данные в бинарном режиме
        with open(путь, 'wb') as файл:
            файл.write(данные)
            
    except PermissionError:
        print(f"Ошибка: нет прав для записи в {путь}", file=sys.stderr)
        sys.exit(1)
    except Exception as ошибка:
        print(f"Ошибка записи файла {путь}: {ошибка}", file=sys.stderr)
        sys.exit(1) 
