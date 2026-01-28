# CryptoCore

Автор: Ivan

Криптографический инструмент для шифрования и дешифрования файлов.

## Установка

```bash
pip install -r requirements.txt
pip install -e .

## Sprint 2: Новые режимы шифрования

### Поддерживаемые режимы:
- **ECB** (Electronic Codebook) - базовый режим
- **CBC** (Cipher Block Chaining) - с цепочкой блоков
- **CFB** (Cipher Feedback) - потоковый режим
- **OFB** (Output Feedback) - потоковый режим
- **CTR** (Counter) - режим счетчика

### Использование новых режимов:

#### CBC шифрование (IV генерируется автоматически):
```bash
cryptocore --algorithm aes --mode cbc --encrypt \
  --key 000102030405060708090a0b0c0d0e0f \
  --input файл.txt \
  --output зашифрованный.bin