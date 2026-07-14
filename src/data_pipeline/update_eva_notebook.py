import json
import os

notebook_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', '01_analisis_eva.ipynb')

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update markdown cell
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        if "- 🗺️ **Departamento**: Valle del Cauca" in "".join(cell['source']):
            new_source = []
            for line in cell['source']:
                if "- ☕ **Cultivos de interés**" in line:
                    new_source.append("- ☕ **Cultivos de interés**: Café, Plátano, Caña, Cacao, Papaya, Fresa, Aguacate, Banano\n")
                else:
                    new_source.append(line)
            cell['source'] = new_source

# Update code cell with COLORS
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        if "COLORS = {" in "".join(cell['source']):
            new_source = []
            in_colors = False
            for line in cell['source']:
                if "COLORS = {" in line:
                    in_colors = True
                    new_source.append("COLORS = {\n")
                    new_source.append("    'Café': '#6F4E37',\n")
                    new_source.append("    'Plátano': '#F2C94C',\n")
                    new_source.append("    'Caña': '#27AE60',\n")
                    new_source.append("    'Cacao': '#8B4513',\n")
                    new_source.append("    'Papaya': '#FF8C00',\n")
                    new_source.append("    'Fresa': '#E32636',\n")
                    new_source.append("    'Aguacate': '#568203',\n")
                    new_source.append("    'Banano': '#FFE135'\n")
                    new_source.append("}\n")
                elif in_colors and "}" in line:
                    in_colors = False
                elif not in_colors:
                    if "CULTIVOS_INTERES =" in line:
                        new_source.append("CULTIVOS_INTERES = ['Café', 'Plátano', 'Caña', 'Cacao', 'Papaya', 'Fresa', 'Aguacate', 'Banano']\n")
                    else:
                        new_source.append(line)
            cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook 01_analisis_eva.ipynb actualizado correctamente.")
