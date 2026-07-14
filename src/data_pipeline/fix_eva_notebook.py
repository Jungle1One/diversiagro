import json
import os
import re

notebook_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', '01_analisis_eva.ipynb')

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "plt.subplots(2, 2" in source and "CULTIVOS_INTERES" in source:
            new_source = []
            
            # Reconstruir las celdas para que usen grid dinámico
            skip_lines = False
            for line in cell['source']:
                if "fig, axes = plt.subplots(2, 2" in line:
                    new_source.append("import math\n")
                    new_source.append("n_cols = 2\n")
                    new_source.append("n_rows = math.ceil(len(CULTIVOS_INTERES) / n_cols)\n")
                    new_source.append("fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 8 * n_rows))\n")
                    new_source.append("axes = axes.flatten()\n")
                elif "ax = axes[idx // 2]" in line:
                    new_source.append(line.replace("axes[idx // 2][idx % 2]", "axes[idx]").replace("axes[idx // 2, idx % 2]", "axes[idx]"))
                elif "plt.tight_layout()" in line:
                    # Añadir código para borrar los axes que sobren antes del tight_layout
                    new_source.append("for idx in range(len(CULTIVOS_INTERES), len(axes)):\n")
                    new_source.append("    fig.delaxes(axes[idx])\n\n")
                    new_source.append(line)
                else:
                    new_source.append(line)
            cell['source'] = new_source

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook 01_analisis_eva.ipynb reparado correctamente. Ahora soporta N cultivos sin romperse.")
