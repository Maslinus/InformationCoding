import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QLineEdit, QPushButton, QLabel, QSpinBox, QComboBox,
                           QMessageBox, QTextEdit)
from PyQt5.QtGui import QFont

def calculate_hamming_bits(data):
    message_length = len(data) # (m)

    check_bit_counter = 0 # (r)

    # Используем формулу Хемминга: 2^r >= m + r + 1
    while 2**check_bit_counter < message_length + check_bit_counter + 1:
        check_bit_counter += 1

    return check_bit_counter

def encode_hamming(data):
    message_length = len(data)
    check_bit_counter = calculate_hamming_bits(data)

    # Создаем массив для закодированных данных
    encoded = ['0'] * (message_length + check_bit_counter)

    # Размещаем информационные биты
    data_index = 0
    for i in range(1, message_length + check_bit_counter + 1):
        # Проверяем, не является ли позиция степенью двойки
        if i & (i - 1) != 0:  
            encoded[i-1] = data[data_index]
            data_index += 1
    
    # Вычисляем контрольные биты
    for i in range(check_bit_counter):
        pos = 2**i  # позиция контрольного бита (1,2,4,8,...)
        xor = 0     # значение контрольного бита
        
        # Проходим по всем битам и проверяем, участвует ли бит в вычислении текущего контрольного бита
        for j in range(1, message_length + check_bit_counter + 1):
            # Если j имеет 1 в позиции pos в двоичном представлении
            if j & pos:
                xor ^= int(encoded[j-1])  # XOR со значением бита
                
        # Записываем значение контрольного бита
        encoded[pos-1] = str(xor)
    
    # Объединяем все биты в строку
    return ''.join(encoded)

def detect_and_correct(encoded):
    length_encoded_message = len(encoded)
    check_bit_counter = calculate_hamming_bits(encoded)
    
    error_position = 0
    for i in range(check_bit_counter):
        pos = 2**i
        xor = 0
        # Проверяем все биты, которые участвуют в текущем контрольном бите
        for j in range(1, length_encoded_message + 1):
            if j & pos:
                xor ^= int(encoded[j-1])
        # Если XOR = 1, значит в этой группе битов есть ошибка
        if xor:
            error_position += pos
    
    if error_position:
        corrected = list(encoded)
        # Инвертируем бит в позиции ошибки
        corrected[error_position-1] = '1' if encoded[error_position-1] == '0' else '0'
        return ''.join(corrected), error_position
    
    # Если ошибок не найдено, возвращаем исходное сообщение
    return encoded, 0

def decode_hamming(encoded):
    length_encoded_message = len(encoded)

    decoded_message = ''
    
    # Извлекаем информационные биты
    # Проходим по всем позициям в закодированном сообщении
    for i in range(1, length_encoded_message + 1):
        # Проверяем, не является ли позиция степенью двойки
        if i & (i - 1) != 0:
            decoded_message += encoded[i-1]
    
    return decoded_message

class HammingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Код Хемминга")
        self.setGeometry(100, 100, 1000, 800)

        self.setStyleSheet("background-color: #878686;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        font = QFont()
        font.setPointSize(14)

        self.lang_label = QLabel("Выберите язык ввода:")
        self.lang_label.setFont(font)
        self.lang_selector = QComboBox()
        self.lang_selector.setFont(font)
        self.lang_selector.setStyleSheet("background-color: white; color: black;")
        self.lang_selector.addItems(["Русский", "English"])
        self.lang_selector.currentIndexChanged.connect(self.on_language_changed)

        self.input_label = QLabel("Введите слово:")
        self.input_label.setFont(font)
        self.input_text = QLineEdit()
        self.input_text.setFont(font)
        self.input_text.setFixedHeight(40)
        self.input_text.setStyleSheet("background-color: white; color: black;")
        self.input_text.textChanged.connect(self.on_text_changed)

        self.binary_label = QLabel("Двоичное представление:")
        self.binary_label.setFont(font)
        self.binary_display = QLineEdit()
        self.binary_display.setFont(font)
        self.binary_display.setFixedHeight(40)
        self.binary_display.setStyleSheet("background-color: white; color: black;")
        self.binary_display.setReadOnly(True)

        self.encode_button = QPushButton("Закодировать")
        self.encode_button.setFont(font)
        self.encode_button.setFixedHeight(50)
        self.encode_button.setStyleSheet("background-color: white; color: black;")
        self.encode_button.clicked.connect(self.encode_message)
        self.encoded_label = QLabel("Закодированное сообщение:")
        self.encoded_label.setFont(font)
        self.encoded_display = QLineEdit()
        self.encoded_display.setFont(font)
        self.encoded_display.setFixedHeight(40)
        self.encoded_display.setStyleSheet("background-color: white; color: black;")
        self.encoded_display.setReadOnly(True)

        self.error_label = QLabel("Выберите позицию ошибки:")
        self.error_label.setFont(font)
        self.error_position = QSpinBox()
        self.error_position.setFont(font)
        self.error_position.setStyleSheet("background-color: white; color: black;")
        self.error_position.setFixedHeight(40)
        self.introduce_error_button = QPushButton("Внести ошибку")
        self.introduce_error_button.setFont(font)
        self.introduce_error_button.setFixedHeight(50)
        self.introduce_error_button.setStyleSheet("background-color: white; color: black;")
        self.introduce_error_button.clicked.connect(self.add_error)

        self.corrupted_label = QLabel("Сообщение с ошибкой:")
        self.corrupted_label.setFont(font)
        self.corrupted_display = QTextEdit()
        self.corrupted_display.setFont(font)
        self.corrupted_display.setFixedHeight(50)
        self.corrupted_display.setStyleSheet("background-color: white; color: black;")
        self.corrupted_display.setReadOnly(True)

        self.correct_button = QPushButton("Исправить ошибку")
        self.correct_button.setFont(font)
        self.correct_button.setFixedHeight(50)
        self.correct_button.setStyleSheet("background-color: white; color: black;")
        self.correct_button.clicked.connect(self.correct_error)
        self.error_pos_label = QLabel("Позиция исправленной ошибки:")
        self.error_pos_label.setFont(font)
        self.error_pos_display = QLineEdit()
        self.error_pos_display.setFont(font)
        self.error_pos_display.setFixedHeight(40)
        self.error_pos_display.setStyleSheet("background-color: white; color: black;")
        self.error_pos_display.setReadOnly(True)

        self.decoded_binary_label = QLabel("Декодированное бинарное сообщение:")
        self.decoded_binary_label.setFont(font)
        self.decoded_binary_display = QLineEdit()
        self.decoded_binary_display.setFont(font)
        self.decoded_binary_display.setFixedHeight(40)
        self.decoded_binary_display.setStyleSheet("background-color: white; color: black;")
        self.decoded_binary_display.setReadOnly(True)
        self.decoded_text_label = QLabel("Декодированный текст:")
        self.decoded_text_label.setFont(font)
        self.decoded_text_display = QLineEdit()
        self.decoded_text_display.setFont(font)
        self.decoded_text_display.setFixedHeight(40)
        self.decoded_text_display.setStyleSheet("background-color: white; color: black;")
        self.decoded_text_display.setReadOnly(True)

        widgets = [
            self.lang_label, self.lang_selector,
            self.input_label, self.input_text,
            self.binary_label, self.binary_display,
            self.encode_button, self.encoded_label, self.encoded_display,
            self.error_label, self.error_position, self.introduce_error_button,
            self.corrupted_label, self.corrupted_display,
            self.correct_button, self.error_pos_label, self.error_pos_display,
            self.decoded_binary_label, self.decoded_binary_display,
            self.decoded_text_label, self.decoded_text_display
        ]

        for widget in widgets:
            layout.addWidget(widget)

    def validate_input(self, text):
        if self.lang_selector.currentText() == "Русский":
            return all(('\u0430' <= c <= '\u044f') for c in text)
        else:
            return all('a' <= c <= 'z' for c in text)

    def text_to_binary(self, text):
        binary = ''
        for char in text:
            if self.lang_selector.currentText() == "Русский":
                val = ord(char) - ord('а')
            else:
                val = ord(char) - ord('a')
            binary += format(val, '06b')
        return binary

    def binary_to_text(self, binary):
        text = ''
        for i in range(0, len(binary), 6):
            chunk = binary[i:i + 6]
            if len(chunk) == 6:
                val = int(chunk, 2)
                if self.lang_selector.currentText() == "Русский":
                    text += chr(val + ord('а'))
                else:
                    text += chr(val + ord('a'))
        return text

    def on_language_changed(self):
        self.input_text.clear()
        self.binary_display.clear()
        self.encoded_display.clear()
        self.corrupted_display.clear()
        self.decoded_binary_display.clear()
        self.decoded_text_display.clear()

    def on_text_changed(self):
        text = self.input_text.text().lower()
        if text:
            if not self.validate_input(text):
                QMessageBox.warning(self, "Ошибка", "Недопустимые символы!")
                self.input_text.setText(text[:-1])
                return
            binary = self.text_to_binary(text)
            self.binary_display.setText(binary)
        else:
            self.binary_display.setText('')

    def encode_message(self):
        binary = self.binary_display.text()
        if binary:
            encoded = encode_hamming(binary)
            self.encoded_display.setText(encoded)
            self.error_position.setMaximum(len(encoded))

    def add_error(self):
        encoded = self.encoded_display.text()
        if encoded:
            pos = self.error_position.value() - 1
            corrupted = list(encoded)
            corrupted[pos] = '1' if encoded[pos] == '0' else '0'
            html_text = ''
            for i, bit in enumerate(corrupted):
                if i == pos:
                    html_text += f'<span style="color: red;">{bit}</span>'
                else:
                    html_text += bit
            self.corrupted_display.setHtml(html_text)
            self.error_position.setMaximum(len(encoded))

    def correct_error(self):
        corrupted = self.corrupted_display.toPlainText()
        if corrupted:
            corrected, pos = detect_and_correct(corrupted)
            decoded_binary = decode_hamming(corrected)
            decoded_text = self.binary_to_text(decoded_binary)
            self.error_pos_display.setText(str(pos))
            self.decoded_binary_display.setText(decoded_binary)
            self.decoded_text_display.setText(decoded_text)

def main():
    app = QApplication(sys.argv)
    window = HammingWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()