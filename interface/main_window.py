from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QFileDialog, QHBoxLayout, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from application.sped_processor import SpedProcessor
from application.exporter import Exporter
from interface.error_window import ErrorWindow


class ValidationThread(QThread):
    progress_signal = Signal(int)
    error_signal = Signal(list)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            processor = SpedProcessor()
            errors = processor.validate_sped(self.file_path, self.progress_signal)
            self.error_signal.emit(errors)
        except Exception as e:
            self.error_signal.emit([f"Erro durante a validação: {str(e)}"])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMSped v25.03.01")
        self.setGeometry(100, 100, 500, 200)

        layout = QVBoxLayout()

        # Layout para seleção de arquivo
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        btn_search = QPushButton("🔍")
        btn_search.clicked.connect(self.import_file)
        file_layout.addWidget(QLabel("Anexe o arquivo:"))
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(btn_search)
        layout.addLayout(file_layout)

        # Layout para barra de progresso e porcentagem
        progress_layout = QVBoxLayout()
        progress_layout.setAlignment(Qt.AlignCenter)  # Centraliza o layout

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFixedSize(300, 20)
        self.progress_bar.setTextVisible(False)  # Oculta a porcentagem dentro da barra
        progress_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Label para exibir a porcentagem
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.progress_label, alignment=Qt.AlignCenter)

        layout.addLayout(progress_layout)

        # Botão de validação
        self.btn_validate = QPushButton("Validar")
        self.btn_validate.clicked.connect(self.validate)
        layout.addWidget(self.btn_validate)

        # Botão para consultar erros
        self.btn_consult_errors = QPushButton("Consultar Erros")
        self.btn_consult_errors.clicked.connect(self.consult_errors)
        self.btn_consult_errors.setEnabled(False)  # Inicialmente desabilitado
        layout.addWidget(self.btn_consult_errors)

        self.setLayout(layout)
        self.errors = []

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo SPED", "", "Arquivos TXT (*.txt)")
        if file_path:
            self.file_path.setText(file_path)

    def validate(self):
        if not self.file_path.text():
            QMessageBox.warning(self, "Aviso!", "Por favor, selecione um arquivo SPED antes de validar.")
            return

        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")  # Reseta o label de porcentagem
        self.errors = []
        self.btn_validate.setEnabled(False)  # Desabilita o botão durante a validação
        self.btn_consult_errors.setEnabled(False)  # Desabilita o botão de consultar erros

        self.validation_thread = ValidationThread(self.file_path.text())
        self.validation_thread.progress_signal.connect(self.update_progress)
        self.validation_thread.error_signal.connect(self.display_errors)
        self.validation_thread.finished.connect(lambda: self.btn_validate.setEnabled(True))  # Reabilita o botão
        self.validation_thread.start()
        self.validation_thread.finished.connect(self.show_completion_message)
        self.validation_thread.start()


    def update_progress(self, percent):
        """Atualiza a barra de progresso e o label de porcentagem."""
        self.progress_bar.setValue(percent)
        self.progress_label.setText(f"{percent}%")  # Atualiza o label com a porcentagem

    def display_errors(self, errors):
        """Recebe os erros e habilita o botão de consultar erros."""
        self.errors = errors
        self.btn_consult_errors.setEnabled(True)  # Habilita o botão de consultar erros

    def consult_errors(self):
        """Abre a janela de erros."""
        if not self.errors:
            QMessageBox.warning(self, "Aviso!", "Nenhum erro encontrado.")
            return

        self.error_window = ErrorWindow(self.errors)
        self.error_window.show()

    def show_completion_message(self):
        """Exibe uma mensagem informando que o arquivo foi verificado."""
        QMessageBox.information(self, "Aviso!", "Arquivo verificado com sucesso!", QMessageBox.Ok)