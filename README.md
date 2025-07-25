# Приложение для работы с кодом Хемминга

## Описание
Графическое приложение для кодирования, обнаружения и исправления ошибок с использованием кода Хемминга. Позволяет:
- Кодировать текстовые сообщения (русские/английские буквы) с добавлением контрольных битов
- Имитировать ошибки передачи данных
- Автоматически обнаруживать и исправлять одиночные ошибки
- Декодировать сообщения обратно в текст

## Основные функции

### Алгоритмы работы
- `calculate_hamming_bits()` - вычисляет необходимое количество контрольных битов
- `encode_hamming()` - кодирует сообщение с добавлением контрольных битов
- `detect_and_correct()` - обнаруживает и исправляет одиночные ошибки
- `decode_hamming()` - декодирует сообщение, удаляя контрольные биты

### Особенности интерфейса
- Поддержка русского и английского языков
- Визуализация битовых последовательностей
- Подсветка ошибочных битов
- Пошаговый процесс кодирования/декодирования
- Адаптивный интерфейс с подсказками

## Инструкция по использованию
1. Выберите язык ввода (русский/английский)
2. Введите текст для кодирования (только буквы выбранного алфавита)
3. Нажмите "Закодировать" для получения защищенного сообщения
4. Укажите позицию и нажмите "Внести ошибку" для имитации ошибки передачи
5. Нажмите "Исправить ошибку" для автоматического исправления
6. Просмотрите декодированное сообщение

## Требования
- Python 3.x
- Библиотеки: PyQt5

## Запуск
```bash
python hamming_app.py
```

Приложение разработано для демонстрации работы корректирующего кода Хемминга в наглядной графической форме.
