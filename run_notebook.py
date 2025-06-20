import papermill as pm
import nbformat
from nbconvert import HTMLExporter

# Voer het notebook uit met papermill, met parameter(s)
pm.execute_notebook(
    'dashboard.ipynb',
    'dashboard_output.ipynb',
    parameters=dict(bestand="dashboard_input.csv")
)

# Laad het uitgevoerde notebook
nb = nbformat.read('dashboard_output.ipynb', as_version=4)

# Maak een HTML-exporter aan
html_exporter = HTMLExporter()

# Converteer notebook naar HTML
(body, resources) = html_exporter.from_notebook_node(nb)

# Sla de HTML op
with open('dashboard_output.html', 'w', encoding='utf-8') as f:
    f.write(body)

print("Notebook uitgevoerd en dashboard_output.html aangemaakt!")
