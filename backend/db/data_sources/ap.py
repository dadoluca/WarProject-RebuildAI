import json
import os
from pathlib import Path

def split_json_by_id_prefix(input_file_path, output_dir='./'):
    """
    Funzione che divide un file JSON in file separati in base al prefisso dell'ID
    
    Args:
        input_file_path (str): Percorso del file JSON di input
        output_dir (str): Directory dove salvare i file risultanti
    """
    # Assicuriamoci che la directory di output esista
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Leggi il file JSON
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Inizializza i dizionari per ciascun tipo di ID
        grouped_data = {
            'uc': [],  # Use cases
            'r': [],   # Rischi
            'b': [],   # Benefici
            'm': []    # Mitigations
        }
        
        # Itera attraverso il file (array di array di oggetti)
        for array_item in data:
            for item in array_item:
                # Estrai il prefisso dall'ID
                if 'metadata' in item and 'id' in item['metadata']:
                    id_value = item['metadata']['id']
                    prefix = ''
                    
                    # Determina il prefisso
                    if id_value.startswith('uc'):
                        prefix = 'uc'
                    elif id_value.startswith('r'):
                        prefix = 'r'
                    elif id_value.startswith('b'):
                        prefix = 'b'
                    elif id_value.startswith('m'):
                        prefix = 'm'
                    
                    # Aggiungi l'oggetto al gruppo corrispondente
                    if prefix and prefix in grouped_data:
                        grouped_data[prefix].append(item)
        
        # Salva ciascun gruppo in un file separato
        for prefix, items in grouped_data.items():
            if items:
                file_name = f"{prefix.upper()}.json"
                file_path = output_path / file_name
                
                with open(file_path, 'a', encoding='utf-8') as output_file:
                    json.dump(items, output_file, indent=2, ensure_ascii=False)
                
                print(f"File {file_name} creato con {len(items)} elementi.")
        
        print("Operazione completata con successo!")
    
    except Exception as error:
        print(f"Errore durante l'elaborazione del file: {error}")

# Esempio di utilizzo:
split_json_by_id_prefix('./threshold_clean_97_group_4.json', './output')