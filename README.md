# Analizador de Secuencias FASTA

Programa de línea de comandos escrito en Python para analizar secuencias de ADN
en formato FASTA.

El programa calcula:

- Longitud de cada secuencia
- Contenido GC
- Filtros opcionales por longitud y contenido GC

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/aagarcia2007/analizador-fasta.git
cd analizador-fasta
uv sync

Uso

Sintaxis general:

uv run python src/analizador.py -i ARCHIVO_FASTA -o ARCHIVO_SALIDA [opciones]

EJEMPLOS:

Analizar todas las secuencias sin filtros:
uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv

Filtrar secuencias de al menos 50 bases:
uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv --min-len 50

Filtrar por contenido GC:
uv run python src/analizador.py -i data/ejemplo.fasta -o resultados.tsv --min-gc 0.4 --max-gc 0.6

Ver ayuda:
uv run python src/analizador.py --help


| Argumento        | Tipo    | Requerido | Descripción                         |
| ---------------- | ------- | --------- | ----------------------------------- |
| `-i`, `--input`  | texto   | Sí        | Ruta del archivo FASTA de entrada   |
| `-o`, `--output` | texto   | Sí        | Ruta del archivo TSV de salida      |
| `--min-len`      | entero  | No        | Longitud mínima                     |
| `--max-len`      | entero  | No        | Longitud máxima                     |
| `--min-gc`       | decimal | No        | Contenido GC mínimo entre 0.0 y 1.0 |
| `--max-gc`       | decimal | No        | Contenido GC máximo entre 0.0 y 1.0 |


Formato de salida

El archivo de salida es un TSV con tres columnas:

encabezado	longitud	contenido_gc
seq1 Homo sapiens BRCA1	78	0.4872
Manejo de errores

Si el archivo de entrada no existe, el programa muestra un mensaje claro:

Error: No se encontró el archivo: data/no_existe.fasta


Documentación técnica:

requisitos.md
diseño.md
