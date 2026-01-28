"""
Парсер аргументов командной строки.
Sprint 2: добавлена поддержка CBC, CFB, OFB, CTR и IV.
Автор: Ivan
"""
import argparse
import os
import sys


def разобрать_аргументы():
    """
    Разбирает и валидирует аргументы командной строки.
    
    Returns:
        dict: словарь с аргументами
        
    Raises:
        SystemExit: если аргументы некорректны
    """
    # Создаем парсер
    парсер = argparse.ArgumentParser(
        prog='cryptocore',
        description='Криптографический инструмент для шифрования файлов'
    )
    
    # Добавляем аргументы согласно требованиям Sprint 2
    
    # --algorithm (обязательный, пока только aes)
    парсер.add_argument(
        '--algorithm',
        required=True,
        choices=['aes'],
        help='Алгоритм шифрования (в данный момент только aes)'
    )
    
    # --mode (обязательный, теперь больше режимов)
    парсер.add_argument(
        '--mode',
        required=True,
        choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'],
        help='Режим работы (ecb, cbc, cfb, ofb, ctr)'
    )
    
    # --encrypt или --decrypt (обязательно один из них)
    группа_операций = парсер.add_mutually_exclusive_group(required=True)
    группа_операций.add_argument(
        '--encrypt',
        action='store_true',
        help='Режим шифрования'
    )
    группа_операций.add_argument(
        '--decrypt',
        action='store_true',
        help='Режим расшифровки'
    )
    
    # --key (обязательный, hex строка)
    парсер.add_argument(
        '--key',
        required=True,
        help='Ключ в шестнадцатеричном формате (32 символа для AES-128)'
    )
    
    # --iv (необязательный для шифрования, обязательный для дешифрования)
    парсер.add_argument(
        '--iv',
        help='Вектор инициализации в шестнадцатеричном формате (32 символа)'
    )
    
    # --input (обязательный, путь к файлу)
    парсер.add_argument(
        '--input',
        required=True,
        help='Путь к входному файлу'
    )
    
    # --output (необязательный, путь к файлу)
    парсер.add_argument(
        '--output',
        help='Путь к выходному файлу (если не указан, будет сгенерирован)'
    )
    
    # Разбираем аргументы
    args = парсер.parse_args()
    
    # Валидация ключа
    try:
        ключ_байты = bytes.fromhex(args.key)
        if len(ключ_байты) != 16:
            print(
                "Ошибка: ключ должен быть 16 байт (32 шестнадцатеричных символа)",
                file=sys.stderr
            )
            sys.exit(1)
    except ValueError:
        print("Ошибка: некорректный шестнадцатеричный формат ключа", 
              file=sys.stderr)
        sys.exit(1)
    
    # Валидация IV если предоставлен
    iv_байты = None
    if args.iv:
        try:
            iv_байты = bytes.fromhex(args.iv)
            if len(iv_байты) != 16:
                print(
                    "Ошибка: IV должен быть 16 байт (32 шестнадцатеричных символа)",
                    file=sys.stderr
                )
                sys.exit(1)
        except ValueError:
            print("Ошибка: некорректный шестнадцатеричный формат IV", 
                  file=sys.stderr)
            sys.exit(1)
    
    # Проверка: IV обязателен для дешифрования
    if args.decrypt and not args.iv:
        # Для режимов с IV, кроме ECB
        if args.mode != 'ecb':
            print(
                f"Ошибка: режим {args.mode} требует --iv для дешифрования",
                file=sys.stderr
            )
            sys.exit(1)
    
    # Проверка: IV не должен быть предоставлен для шифрования
    if args.encrypt and args.iv:
        print(
            "Предупреждение: IV предоставлен для шифрования. IV будет сгенерирован автоматически.",
            file=sys.stderr
        )
        # Всё равно используем предоставленный IV для единообразия
        # iv_байты уже установлен выше
    
    # Проверка существования входного файла
    if not os.path.exists(args.input):
        print(f"Ошибка: входной файл не найден: {args.input}", 
              file=sys.stderr)
        sys.exit(1)
    
    # Генерация имени выходного файла, если не указано
    if not args.output:
        if args.encrypt:
            args.output = args.input + '.enc'
        else:
            # Если файл заканчивается на .enc, убираем это расширение
            if args.input.endswith('.enc'):
                args.output = args.input[:-4]
            else:
                args.output = args.input + '.dec'
    
    # Возвращаем словарь с аргументами
    return {
        'algorithm': args.algorithm,
        'mode': args.mode,
        'encrypt': args.encrypt,
        'key': args.key,
        'key_bytes': ключ_байты,
        'iv': args.iv,
        'iv_bytes': iv_байты,
        'input': args.input,
        'output': args.output
    }