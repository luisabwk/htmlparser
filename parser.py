import os
import json
from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def process_json_files(input_folder, output_folder):
    # Expande o caminho do diretório home, se necessário
    input_folder = os.path.expanduser(input_folder)
    output_folder = os.path.expanduser(output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            with open(input_file_path, 'r', encoding='utf-8') as file:
                json_content = json.load(file)
            
            # Processa o conteúdo do JSON para remover HTML
            cleaned_json_content = {}
            for key, value in json_content.items():
                if isinstance(value, str):
                    cleaned_json_content[key] = clean_html(value)
                else:
                    cleaned_json_content[key] = value
            
            output_filename = f"{os.path.splitext(filename)[0]}_cleaned.json"
            output_file_path = os.path.join(output_folder, output_filename)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(cleaned_json_content, output_file, ensure_ascii=False, indent=4)
            print(f"Processado: {filename}, salvo como: {output_filename}")

# Exemplo de uso
input_folder = '~/Desktop/glossario_printi'  # Caminho para a pasta de entrada
output_folder = '~/Desktop/parsedGlossarioPrinti'  # Caminho para a pasta de saída

process_json_files(input_folder, output_folder)