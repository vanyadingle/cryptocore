# CryptoCore

**Автор:** Ivan  
**Версия:** 1.0.0

Криптографический инструмент командной строки для шифрования, дешифрования и хеширования данных.

---

##  Установка

```bash
# Клонирование репозитория
git clone https://github.com/ivan/cryptocore.git
cd cryptocore

# Виртуальное окружение (рекомендуется)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Установка зависимостей и пакета
pip install -r requirements.txt
pip install -e .
## Быстрый старт
Шифрование файла
bash
# С автоматической генерацией ключа
cryptocore encrypt --algorithm aes --mode cbc --encrypt --input secret.txt

# С указанием ключа
cryptocore encrypt --algorithm aes --mode cbc --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input secret.txt
Дешифрование файла
bash
cryptocore encrypt --algorithm aes --mode cbc --decrypt \
  --key 8bf1b5f2fa540cd56901a1ccf50409f5 \
  --iv 72718d608d344602ffdeaf318d96f34b \
  --input secret.txt.enc
Хеширование файла
bash
cryptocore dgst --algorithm sha256 --input document.pdf
## Команды
encrypt - Шифрование/дешифрование
Синтаксис: cryptocore encrypt [ОПЦИИ]

Опция	Описание
--algorithm aes	Алгоритм шифрования
--mode MODE	Режим (ecb, cbc, cfb, ofb, ctr)
--encrypt / --decrypt	Операция
--input FILE	Входной файл
--key KEY	Ключ в hex (генерируется автоматически)
--iv IV	Вектор инициализации
--output FILE	Выходной файл
dgst - Хеширование
Синтаксис: cryptocore dgst [ОПЦИИ]

Опция	Описание
--algorithm sha256, simple	Алгоритм хеширования
--input FILE	Входной файл (или '-' для stdin)
--output FILE	Сохранить хеш в файл
## Режимы шифрования
Режим	Описание	Padding
ECB	Electronic Codebook	Да
CBC	Cipher Block Chaining	Да
CFB	Cipher Feedback	Нет
OFB	Output Feedback	Нет
CTR	Counter	Нет
## Примеры
Шифрование с авто-ключом
bash
cryptocore encrypt --algorithm aes --mode ctr --encrypt --input secret.txt
# Вывод: [INFO] Сгенерирован случайный ключ: 8bf1b5f2fa540cd56901a1ccf50409f5
Хеш из stdin
bash
echo -n "Hello, World!" | cryptocore dgst --algorithm sha256 --input -
Сохранение хеша в файл
bash
cryptocore dgst --algorithm sha256 --input backup.tar --output backup.sha256
Работа с большими файлами
bash
cryptocore encrypt --algorithm aes --mode ctr --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input movie.mp4 \
  --output movie.enc
## Структура проекта
text
cryptocore/
├── cryptocore/          # Основной пакет
│   ├── main.py          # Главная точка входа
│   ├── cli.py           # Парсер для шифрования
│   ├── cli_dgst.py      # Парсер для хеширования
│   ├── file_io.py       # Работа с файлами
│   └── crypto/          # Криптографические модули
│       ├── aes.py       # AES-128
│       ├── csprng.py    # Генерация случайных чисел
│       ├── modes.py     # Режимы шифрования
│       ├── padding.py   # PKCS#7
│       └── hash/        # Хеш-функции
│           ├── sha256_fixed.py  # SHA-256 через hashlib
│           └── simple_hash.py    # Упрощенная хеш-функция
├── tests/               # Тесты
├── requirements.txt     # Зависимости
├── setup.py             # Установка пакета
└── README.md            # Этот файл
## Тестирование
bash
# Запуск тестов
python tests/test_basic.py
python tests/test_csprng.py

# Через pytest
python -m pytest tests/ -v
Проверка SHA-256
bash
echo -n "abc" | cryptocore dgst --algorithm sha256 --input -
# Ожидается: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
Round-trip тест
bash
echo "test" > test.txt
cryptocore encrypt --algorithm aes --mode cbc --encrypt --input test.txt
# Сохраните KEY и IV из вывода
cryptocore encrypt --algorithm aes --mode cbc --decrypt \
  --key KEY --iv IV --input test.txt.enc --output test_dec.txt
diff test.txt test_dec.txt  # Должно быть пусто
## Требования
Python 3.8+

pycryptodome

bash
pip install pycryptodome
## Устранение проблем
Команда не найдена
bash
pip install -e .
python -m cryptocore.main --help
Неправильные хеши SHA-256
Используется hashlib для гарантии правильности. Собственная реализация в разработке.

## Реализовано
Sprint 1: AES-128, ECB режим, PKCS#7
Sprint 2: CBC, CFB, OFB, CTR режимы, IV
Sprint 3: CSPRNG, автогенерация ключей
Sprint 4: Хеш-функции (SHA-256, SimpleHash)

В разработке: HMAC, GCM, PBKDF2