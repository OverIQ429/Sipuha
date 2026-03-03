# check_torchcodec.py
import sys

print("Проверка доступности torchcodec...")

# 1. Проверяем torchaudio
try:
    import torchaudio

    print(f"✓ torchaudio установлен: {torchaudio.__version__}")

    # Проверяем доступные бэкенды
    print(f"  Доступные бэкенды: {torchaudio.list_audio_backends()}")

    # Пробуем установить soundfile бэкенд
    try:
        torchaudio.set_audio_backend("soundfile")
        print("  ✓ soundfile бэкенд установлен")
    except:
        print("  ✗ Не удалось установить soundfile бэкенд")

except ImportError:
    print("✗ torchaudio не установлен")
    print("  Установите: pip install torchaudio --index-url https://download.pytorch.org/whl/cpu")

# 2. Проверяем torchcodec напрямую
try:
    import torchcodec

    print(
        f"✓ torchcodec установлен: {torchcodec.__version__ if hasattr(torchcodec, '__version__') else 'версия неизвестна'}")
except ImportError:
    print("✗ torchcodec не установлен напрямую")
    print("  Это нормально, обычно он идет в составе torchaudio")

# 3. Проверяем FFmpeg
import subprocess

try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ FFmpeg найден")
        # Выводим первую строку с версией
        lines = result.stdout.split('\n')
        if lines:
            print(f"  Версия: {lines[0][:50]}...")
    else:
        print("✗ FFmpeg не найден или не работает")
except:
    print("✗ FFmpeg не установлен")
    print("  Скачайте с: https://github.com/BtbN/FFmpeg-Builds/releases")
    print("  И добавьте в PATH")

# 4. Проверяем работу torchaudio.load
print("\nТест работы torchaudio.load...")
try:
    import tempfile
    import numpy as np
    import soundfile as sf

    # Создаем тестовый WAV файл
    temp_dir = tempfile.mkdtemp()
    test_file = temp_dir + "/test.wav"

    # Генерируем тестовый сигнал
    sr = 16000
    t = np.linspace(0, 1, sr)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t)  # Синусоида 440 Гц

    sf.write(test_file, signal, sr)

    # Пробуем загрузить через torchaudio
    waveform, sample_rate = torchaudio.load(test_file)
    print(f"✓ torchaudio.load работает!")
    print(f"  Загружено: {waveform.shape} сэмплов, {sample_rate} Гц")

    import os

    os.remove(test_file)
    os.rmdir(temp_dir)

except Exception as e:
    print(f"✗ torchaudio.load не работает: {e}")
    print("  Рекомендация: используйте альтернативный метод с librosa")

print("\n=== РЕЗЮМЕ ===")
print("Если torchcodec не устанавливается, лучше использовать:")
print("1. torchaudio с soundfile бэкендом")
print("2. Или полностью обойти pyara, используя librosa")