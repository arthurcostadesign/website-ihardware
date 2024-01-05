import os
import json
from jinja2 import Environment, FileSystemLoader

# Carrega os dados do arquivo JSON
json_file = r"D:\Usuários\Arthur\Área de Trabalho\iHARDware! - pré-processamento\intel\dados_processadores_intel.json"
with open(json_file, "r", encoding="utf-8") as file:
    processors_data = json.load(file)

# Configuração do ambiente Jinja2
template_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("template_intel.html")

# Cria a pasta "pages" se não existir
output_folder = "pages/intel_cpu"
os.makedirs(output_folder, exist_ok=True)

# Itera sobre a lista de processadores e gera as páginas HTML
for processor_data in processors_data:
    output_file_path = os.path.join(
        output_folder, f"{processor_data['numero_do_processador']}.html"
    )
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(template.render(data=processor_data))

    print(f"Página gerada com sucesso em: {output_file_path}")
