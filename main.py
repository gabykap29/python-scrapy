import requests
from bs4 import BeautifulSoup
import json

# URL elegida
url = input('Ingrese la url: ')

# Request
res = requests.get(url, verify=False)
res.raise_for_status()  # Verificar si la solicitud fue exitosa

# Obtener texto plano y dárselo a BeautifulSoup
soup = BeautifulSoup(res.text, 'html.parser')

# Obtener todos los <a>
results = soup.find_all('a')

array = []

# Ingresar a cada <a>
for result in results:
    href = result.get('href', '')
    if href and href not in ['#', 'javascript:void(0)'] and href.startswith(('http://', 'https://')) and 'mailto' not in href and 'tel' not in href:
        try:
            response = requests.get(href)
            response.raise_for_status()
            content = BeautifulSoup(response.text, 'html.parser')
            titles = [title.get_text() for title in content.find_all('h1')]
            paragraphs = [p.get_text() for p in content.find_all('p')]
            array.append({'url': href, 'titles': titles, 'paragraphs': paragraphs})
        except requests.RequestException as e:
            print(f"Error al acceder a {href}: {e}")

# Convertir a JSON
results_json = json.dumps(array, ensure_ascii=False, indent=4)

# Crear el JSON
with open('./contenido.json', 'w', encoding='utf-8') as file_json:
    file_json.write(results_json)

# Imprimir resultados
print(results_json)
