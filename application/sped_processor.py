import time
from application.sped_errors import SpedErrors

def parse_float(value):
    """ Converte string para float, tratando valores vazios """
    try:
        return float(value.replace(",", ".")) if value.strip() else 0.0
    except ValueError:
        return 0.0

class SpedProcessor:
    def validate_sped(self, file_path, progress_signal):
        errors = SpedErrors()
        vl_doc_map = {}  # Dicionário para armazenar VL_DOC por número de documento
        last_num_doc = None  # Variável para armazenar o último número de documento C100
        
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as file:
            lines = file.readlines()
            total_lines = len(lines)
            
            for i, line in enumerate(lines):
                parts = line.strip().split('|')
                
                if len(parts) > 12 and parts[1] == "C100":
                    last_num_doc = parts[8]  # Número do documento
                    vl_doc = parse_float(parts[12])
                    vl_doc_map[last_num_doc] = vl_doc  # Armazena VL_DOC com o número do documento
                
                if len(parts) > 5 and parts[1] == "C190" and last_num_doc:
                    vl_opr = parse_float(parts[5])  # Corrigido índice para 5
                    
                    if last_num_doc in vl_doc_map and vl_doc_map[last_num_doc] != vl_opr:
                        errors.add_error(f"Divergência encontrada no doc {last_num_doc}: VL_DOC ({vl_doc_map[last_num_doc]}) ≠ VL_OPR ({vl_opr})")
                
                # Atualiza a barra de progresso
                percent = int(((i + 1) / total_lines) * 100)
                progress_signal.emit(percent)
                
                time.sleep(0.01)  # Simula o processamento
        
        return errors.get_errors()