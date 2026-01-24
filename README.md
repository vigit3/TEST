Es un script en Python para “corporatizar” archivos de combos `email:password`, eliminando correos de dominios gratuitos/conocidos y dejando principalmente posibles correos **corporativos**. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)

### ¿Qué hace el script?

- Lee archivos (o una carpeta de archivos) con líneas tipo `email:password` y normaliza separadores como `, | espacio` a `:`. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)  
- Valida que cada línea tenga formato correcto de email y descarta líneas vacías o mal formadas. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)
- Excluye una lista extensa de dominios gratuitos, temporales y typos comunes (gmail, hotmail, yahoo, protonmail, yopmail, mailinator, etc.). [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)
- Conserva las líneas restantes como posibles correos corporativos y las guarda en un nuevo archivo con sufijo `_corporatizado`. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)

### Estadísticas y salida

- Genera un archivo de salida con encabezado descriptivo, fecha de análisis y estadísticas de limpieza (totales leídos, válidos, removidos por formato, removidos por dominio y líneas finales). [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)
- Incluye un resumen de distribución por dominio (conteo y porcentaje) de los correos que quedaron tras la limpieza. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)
- Si se procesa una carpeta, crea además un `global_corporatizado.txt` con el consolidado de todos los archivos ya limpiados, sin duplicados, más estadísticas globales por dominio. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)

### Uso e idioma

- Uso básico: `python corporatizarv2.py ruta_entrada [es|en]`. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)  
- Soporta español e inglés para todos los mensajes, descripciones y encabezados de los archivos generados. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)
- Los textos se acreditan a @BlackHat_RedCat en la descripción y en los headers de salida. [raw.githubusercontent](https://raw.githubusercontent.com/Cocomx/TEST/refs/heads/main/corporatizarv2.py)
