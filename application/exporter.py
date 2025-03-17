import csv

class Exporter:
    @staticmethod
    def export_to_csv(errors, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Erros encontrados"])
            for error in errors:
                writer.writerow([error])
