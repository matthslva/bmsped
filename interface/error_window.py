from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QFileDialog
from application.exporter import Exporter


class ErrorWindow(QWidget):
    def __init__(self, errors):
        super().__init__()
        self.setWindowTitle("Erros Encontrados")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Lista de erros
        self.error_list = QTextEdit()
        self.error_list.setReadOnly(True)
        layout.addWidget(self.error_list)

        # Botão de exportação
        self.btn_export = QPushButton("Exportar Erros")
        self.btn_export.clicked.connect(self.export_errors)
        layout.addWidget(self.btn_export)

        self.setLayout(layout)
        self.errors = errors
        self.display_errors()

    def display_errors(self):
        """Exibe os erros na QTextEdit."""
        self.error_list.clear()
        for error in self.errors:
            self.error_list.append(error)

    def export_errors(self):
        """Exporta os erros para um arquivo CSV."""
        if not self.errors:
            QMessageBox.warning(self, "Aviso", "Nenhum erro para exportar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Erros", "", "Arquivos CSV (*.csv)")
        if file_path:
            Exporter.export_to_csv(self.errors, file_path)
            QMessageBox.information(self, "Sucesso", "Erros exportados com sucesso!")